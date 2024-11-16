import { NextRequest, NextResponse } from "next/server";
import {
  FusionSDK,
  NetworkEnum,
  OrderStatus,
  PrivateKeyProviderConnector,
  Web3Like,
} from "@1inch/fusion-sdk";
import { formatUnits, JsonRpcProvider } from "ethers";

const PRIVATE_KEY = process.env.PRIVATE_KEY!;
const NODE_URL = process.env.NODE_URL!;
const DEV_PORTAL_API_TOKEN = process.env.DEV_PORTAL_API_TOKEN!;

const ethersRpcProvider = new JsonRpcProvider(NODE_URL);

const ethersProviderConnector: Web3Like = {
  eth: {
    call(transactionConfig): Promise<string> {
      return ethersRpcProvider.call(transactionConfig);
    },
  },
  extend(): void {},
};

const connector = new PrivateKeyProviderConnector(
  PRIVATE_KEY,
  ethersProviderConnector,
);

const sdk = new FusionSDK({
  url: "https://api.1inch.dev/fusion",
  network: NetworkEnum.POLYGON,
  blockchainProvider: connector,
  authKey: DEV_PORTAL_API_TOKEN,
});

export async function POST(request: NextRequest) {
  try {
    const { fromTokenAddress, toTokenAddress, amount, walletAddress } =
      await request.json();

    if (!fromTokenAddress || !toTokenAddress || !amount || !walletAddress) {
      return NextResponse.json({ error: "Missing required parameters" }, {
        status: 400,
      });
    }

    const params = {
      fromTokenAddress,
      toTokenAddress,
      amount,
      walletAddress,
      source: "sdk-test",
    };

    const quote = await sdk.getQuote(params);

    const dstTokenDecimals = 18;
    const recommendedPreset = quote.presets[quote.recommendedPreset];
    if (!recommendedPreset) {
      return NextResponse.json({
        error: "No recommended preset found",
      }, {
        status: 400,
      });
    }

    const auctionStartAmount = formatUnits(
      recommendedPreset.auctionStartAmount,
      dstTokenDecimals,
    );
    const auctionEndAmount = formatUnits(
      recommendedPreset.auctionEndAmount,
      dstTokenDecimals,
    );

    const preparedOrder = await sdk.createOrder(params);
    const info = await sdk.submitOrder(
      preparedOrder.order,
      preparedOrder.quoteId,
    );

    const start = Date.now();
    let statusMessage = "Unknown";
    let fills = null;

    while (true) {
      try {
        const data = await sdk.getOrderStatus(info.orderHash);

        if (data.status === OrderStatus.Filled) {
          statusMessage = "Order Filled";
          fills = data.fills;
          break;
        }

        if (data.status === OrderStatus.Expired) {
          statusMessage = "Order Expired";
          break;
        }

        if (data.status === OrderStatus.Cancelled) {
          statusMessage = "Order Cancelled";
          break;
        }
      } catch (e) {
        console.error(e);
      }
    }

    const elapsedTime = (Date.now() - start) / 1000;

    return NextResponse.json({
      orderHash: info.orderHash,
      auctionStartAmount,
      auctionEndAmount,
      statusMessage,
      fills,
      elapsedTime,
    });
  } catch (error) {
    console.error(error);
    return NextResponse.json({ error: "Internal Server Error" }, {
      status: 500,
    });
  }
}

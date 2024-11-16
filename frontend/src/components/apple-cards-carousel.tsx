"use client";
import React from "react";
import { Card, Carousel } from "@/components/ui/apple-cards-carousel";

export default function AppleCardsCarousel() {
  const cards = data.map((card, index) => (
    <Card key={card.src} card={card} index={index} layout={true} />
  ));

  return (
    <div className="w-full h-full py-20" id="features">
      <h2 className="max-w-7xl pl-4 mx-auto text-xl md:text-5xl font-bold text-neutral-800 dark:text-neutral-200 font-sans">
        Features
      </h2>
      <Carousel items={cards} />
    </div>
  );
}

const titleToExtendedDescription = {
  "ai-suggestions":
    "Leverage the power of AI-driven insights to supercharge your decision-making process. Our advanced algorithms analyze your portfolio comprehensively, identifying key opportunities and providing tailored suggestions to help you maximize returns while minimizing risks. Say goodbye to guesswork and welcome a data-backed approach that empowers you to make smarter, more informed investment decisions with confidence.",
  "track-portfolio":
    "Stay in complete control of your investments with real-time portfolio tracking. Our state-of-the-art platform offers instant updates, detailed analytics, and actionable insights that ensure you are always informed about the performance and health of your portfolio. Make timely adjustments and capitalize on opportunities without any delays, empowering you to achieve your financial goals effectively.",
  "rebalance-portfolio":
    "Maintain an optimal portfolio with our expert-guided rebalancing tools designed to align with your unique risk appetite and financial objectives. Our platform analyzes your investments and provides tailored recommendations for reallocating assets to maximize returns and manage risks. Whether you're a conservative or aggressive investor, our rebalancing strategies keep you on track to achieve your financial aspirations.",
  "defi-strategies":
    "Unlock the full potential of decentralized finance with our curated selection of advanced DeFi strategies. From yield farming to liquidity provision, we equip you with cutting-edge insights and actionable recommendations to navigate the dynamic DeFi landscape. Empower yourself to make informed decisions, seize lucrative opportunities, and optimize your financial growth in the ever-evolving world of DeFi.",
  "execute-trades":
    "Experience seamless and hassle-free trading with our streamlined execution tools. With just a few clicks, you can perform transactions efficiently while leveraging our intelligent suggestions to optimize every trade. Whether you're buying, selling, or rebalancing, our intuitive platform ensures that your trading experience is not only smooth but also strategically aligned with your investment goals.",
} as const;

const DummyContent = ({
  kind,
}: {
  kind: keyof typeof titleToExtendedDescription;
}) => {
  return (
    <div
      key={"dummy-content"}
      className="bg-[#F5F5F7] p-8 md:p-14 rounded-3xl mb-4"
    >
      <p className="text-neutral-600 text-base md:text-2xl font-sans max-w-3xl mx-auto">
        {titleToExtendedDescription[kind]}
      </p>
    </div>
  );
};

const data = [
  {
    category: "AI powered suggestions",
    title: "Based on your portfolio.",
    src: "/london.jpeg",
    content: <DummyContent kind="ai-suggestions" />,
  },
  {
    category: "Track your portfolio",
    title: "In real-time, no delays, only insights.",
    src: "/surf.jpeg",
    content: <DummyContent kind="track-portfolio" />,
  },
  {
    category: "Rebalance your portfolio",
    title: "Suited to your risk appetite.",
    src: "/path.jpeg",
    content: <DummyContent kind="rebalance-portfolio" />,
  },
  {
    category: "DeFi strategies",
    title: "Advanced strategies for everyone.",
    src: "/seal.jpeg",
    content: <DummyContent kind="defi-strategies" />,
  },
  {
    category: "Execute trades",
    title: "With a few clicks, without any hassle.",
    src: "/beach.jpeg",
    content: <DummyContent kind="execute-trades" />,
  },
];

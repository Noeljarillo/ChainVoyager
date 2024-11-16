import "./globals.css";
import "@rainbow-me/rainbowkit/styles.css";

import { headers } from "next/headers";

import { Inter } from "next/font/google";
import Providers from "@/app/providers";

const inter = Inter({ subsets: ["latin"] });

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const cookie = (await headers()).get("cookie");

  return (
    <html lang="en">
      <body className={`${inter.className} scroll-smooth`}>
        <Providers cookie={cookie}>{children}</Providers>
      </body>
    </html>
  );
}

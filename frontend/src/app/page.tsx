import AppleCardsCarousel from "@/components/apple-cards-carousel";
import BentoGrid from "@/components/bento-grid";
import Navbar from "@/components/floating-navbar";
import GoogleGeminiEffect from "@/components/google-gemini-effect";
import { FooterComponent } from "@/components/footer";

export default function Home() {
  return (
    <>
      <Navbar />
      <GoogleGeminiEffect />
      <AppleCardsCarousel />
      <BentoGrid />
      <FooterComponent />
    </>
  );
}

"use client";
import React from "react";
import { FloatingNav as UIFloatingNav } from "@/components/ui/floating-navbar";
import { IconHome, IconMessage, IconUser } from "@tabler/icons-react";

export default function FloatingNav({ alwaysVisible }: {
  alwaysVisible?: boolean;
}) {
  const navItems = [
    {
      name: "Home",
      link: "/",
      icon: <IconHome className="h-4 w-4 text-neutral-500 dark:text-white" />,
    },
    {
      name: "Features",
      link: "/#features",
      icon: <IconUser className="h-4 w-4 text-neutral-500 dark:text-white" />,
    },
    {
      name: "Stats",
      link: "/#stats",
      icon:
      <IconMessage className="h-4 w-4 text-neutral-500 dark:text-white" />,
    },
  ];
  return (
    <div className="relative  w-full">
      <UIFloatingNav navItems={navItems} alwaysVisible={alwaysVisible} />
    </div>
  );
}

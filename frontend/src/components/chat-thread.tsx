"use client";
import { Thread } from "@assistant-ui/react";
import "@assistant-ui/react/styles/index.css";
import { MarkdownText } from "@/components/ui/markdown-to-text";
import CustomMarkdownText from "@/components/markdown-text";
import React, { useContext, useEffect, useState } from "react";
import { Sidebar, SidebarBody, SidebarLink } from "@/components/ui/sidebar";
import { IconHome } from "@tabler/icons-react";
import { cn } from "@/lib/utils";
import { GraphContext } from "@/app/providers";

export type ChatComponentProps = Parameters<typeof ChatComponent>[0];

export default function ChatComponent({ links, graphs }: {
  links: {
    label: string;
    href: string;
    icon: JSX.Element;
  }[];
  graphs: React.ReactNode[];
}) {
  const [open, setOpen] = useState(false);
  const { graphs: contextGraphs } = useContext(GraphContext);

  useEffect(() => {
    if (!open && contextGraphs.length > 0) {
      setOpen(true);
    }
  }, [contextGraphs, open]);

  return (
    <>
      <div
        className={cn(
          "rounded-md flex flex-col md:flex-row bg-gray-100 dark:bg-neutral-800 w-full flex-1 mx-auto border border-neutral-200 dark:border-neutral-700 overflow-hidden",
          "h-screen",
        )}
      >
        <Sidebar open={open} setOpen={setOpen}>
          <SidebarBody className="justify-between gap-10">
            <div className="flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
              <div className="mt-8 flex flex-col gap-2">
                {links.map((link, idx) => (
                  <SidebarLink
                    key={`link-${idx}`}
                    link={link}
                  >
                    {link.label === "Charts" &&
                      graphs.map((graph, idx) => (
                        <div key={`graph-${idx}`} className="mt-8">
                          {graph}
                        </div>
                      ))}
                  </SidebarLink>
                ))}
              </div>
            </div>
            <div>
              <SidebarLink
                link={{
                  label: "Home",
                  href: "/",
                  icon: (
                    <IconHome className="text-neutral-700 dark:text-neutral-200 h-5 w-5 flex-shrink-0" />
                  ),
                }}
              />
            </div>
          </SidebarBody>
        </Sidebar>
        <div className="h-full w-full">
          <Thread
            assistantMessage={{
              components: { Text: (CustomMarkdownText as typeof MarkdownText) },
            }}
          />
        </div>
      </div>
    </>
  );
}

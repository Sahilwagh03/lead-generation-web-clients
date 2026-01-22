import React, { ReactNode } from 'react'
import { AppSidebar } from "@/components/app-sidebar"
import { Separator } from "@/components/ui/separator"
import {
    SidebarInset,
    SidebarProvider,
    SidebarTrigger,
} from "@/components/ui/sidebar"
import { DynamicBreadcrumb } from '@/components/dynamicBreadcrumb'

type Props = {
    children: ReactNode
}

function DashboardLayout({ children }: Props) {
    return (
        <SidebarProvider>
            <AppSidebar />
            <SidebarInset className='contain-inline-size'>
                <header className="flex h-16 shrink-0 bg-white dark:bg-black items-center gap-2 transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-12 sticky top-0 z-20">
                    <div className="flex items-center gap-2 px-4">
                        <SidebarTrigger className="-ml-1" />
                        <Separator orientation="vertical" className="mr-2 h-4" />
                        <DynamicBreadcrumb/>
                    </div>
                </header>
                <div className="p-4 pt-0">
                    {children}
                </div>
            </SidebarInset>
        </SidebarProvider>
    )
}

export default DashboardLayout
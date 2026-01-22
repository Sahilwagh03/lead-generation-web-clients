"use client"

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

const TabView = () => {
  return (
    <Tabs defaultValue="today" className="w-fit">
      <TabsList className="grid w-full grid-cols-2">
        <TabsTrigger value="today">Today</TabsTrigger>
        <TabsTrigger value="tomorrow">Tomorrow</TabsTrigger>
      </TabsList>

      <TabsContent value="today">

      </TabsContent>

      <TabsContent value="tomorrow">
      </TabsContent>
    </Tabs>
  )
}

export default TabView

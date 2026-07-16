import Sidebar from "./components/Sidebar";

import {  Outlet } from "react-router";

export default function App() {
  return (
    <div className="flex h-screen">
      <Sidebar />
      <div className="flex-1">
        <h1 className="font-bold text-xl mr-8">Admin Dashboard</h1>
        <Outlet />
      </div>
    </div>
  );
}

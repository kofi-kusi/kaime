import Sidebar from "../components/Sidebar";
import { Outlet } from "react-router";

export default function Dashboard() {
  return (
    <div className="flex">
      <Sidebar />
      <main className="lg:min-w-3xl mx-auto">
        <Outlet />
      </main>
    </div>
  );
}

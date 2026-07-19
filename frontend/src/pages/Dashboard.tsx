import Sidebar from "../components/Sidebar";
import ThemeToggler from "../components/ThemeToggler";
import { Outlet } from "react-router";

export default function Dashboard() {
  return (
    <div className="flex bg-app-bg min-h-screen text-app-text">
      <Sidebar />
      <main className="flex-1 p-8">
        <header className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-app-text-h">Dashboard</h1>
            <p className="text-app-text">
              Welcome to your academic management hub.
            </p>
          </div>
          <ThemeToggler />
        </header>

        <section className="bg-app-bg p-6 rounded-xl border border-app-border shadow-app-shadow">
          <Outlet />
        </section>
      </main>
    </div>
  );
}

import { Link, Outlet } from "react-router";
import ThemeToggler from "./components/ThemeToggler";

export default function App() {
  return (
    <div className="min-h-screen bg-app-bg text-app-text font-sans">
      {/* Navigation */}
      <nav className="border-b border-app-border sticky top-0 z-50 bg-app-bg/80 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-2xl font-bold text-app-text-h">Kaime</span>
          </div>
          <div className="flex items-center gap-6">
            <a
              href="#features"
              className="text-app-text hover:text-app-accent transition-colors font-medium"
            >
              Features
            </a>
            <ThemeToggler />
            <Link
              to="/dashboard"
              className="bg-app-accent text-white px-5 py-2 rounded-lg font-medium hover:bg-blue-700 transition shadow-sm"
            >
              Dashboard
            </Link>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-6 py-16">
        {/* Hero */}
        <section className="text-center mb-24">
          <h1 className="text-6xl md:text-7xl font-extrabold text-app-text-h mb-6 leading-tight tracking-tight">
            Automate Academic <br />
            <span className="text-app-accent">Notifications</span>
          </h1>
          <p className="text-xl text-app-text max-w-2xl mx-auto mb-10">
            Keep students informed without the manual effort. Kaime streamlines
            university event alerts, deadline reminders, and academic news with
            smart scheduling.
          </p>
          <div className="flex gap-4 justify-center">
            <Link
              to="/dashboard"
              className="bg-app-accent text-white px-8 py-3 rounded-xl font-semibold text-lg hover:bg-blue-700 transition shadow-lg"
            >
              Launch Dashboard
            </Link>
          </div>
        </section>

        {/* Features Grid */}
        <section id="features" className="grid md:grid-cols-3 gap-8 py-12">
          {[
            {
              icon: "📅",
              title: "Event Scheduling",
              desc: "Create events once and let Kaime handle the notification timeline automatically.",
            },
            {
              icon: "🎓",
              title: "Targeted Alerts",
              desc: "Ensure the right information reaches the right students at the perfect time.",
            },
            {
              icon: "⚡",
              title: "Smart Automation",
              desc: "Reduce manual communication overhead with intelligent scheduling.",
            },
          ].map((feat, i) => (
            <div
              key={i}
              className="p-8 rounded-2xl border border-app-border bg-app-bg shadow-app-shadow hover:border-app-accent/50 transition-colors"
            >
              <div className="text-app-accent mb-4 text-3xl">{feat.icon}</div>
              <h3 className="text-xl font-bold mb-3 text-app-text-h">
                {feat.title}
              </h3>
              <p className="text-app-text">{feat.desc}</p>
            </div>
          ))}
        </section>

        <div className="mt-12">
          <Outlet />
        </div>
      </main>

      <footer className="border-t border-app-border py-12">
        <div className="max-w-7xl mx-auto px-6 text-center text-app-text">
          <p>
            &copy; {new Date().getFullYear()} Kaime Academic Solutions. All
            rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}

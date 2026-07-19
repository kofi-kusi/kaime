import React, { useState, useEffect } from "react";
import { api, type Subscriber } from "../api";

export default function SubscribersView() {
  const [subscribers, setSubscribers] = useState<Subscriber[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState<Partial<Subscriber>>({});

  const loadSubscribers = async () => {
    const data = await api.getSubscribers();
    setSubscribers(data);
  };

  useEffect(() => {
    loadSubscribers();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.createSubscriber(formData as Subscriber);
      setShowForm(false);
      setFormData({});
      loadSubscribers();
    } catch (error) {
      alert(`Error creating subscriber: ${error}`);
    }
  };

  const handleDelete = async (email: string) => {
    if (window.confirm("Delete this subscriber?")) {
      await api.deleteSubscriber(email);
      loadSubscribers();
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-app-text-h">Subscribers</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-app-accent text-white px-5 py-2 rounded-lg font-medium hover:opacity-90 transition shadow-sm"
        >
          {showForm ? "Cancel" : "Add Subscriber"}
        </button>
      </div>

      {showForm && (
        <div className="flex justify-center mb-6">
          <form
            onSubmit={handleCreate}
            className="w-full max-w-2xl bg-app-bg p-6 rounded-xl border border-app-border shadow-app-shadow"
          >
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <input
                required
                placeholder="Email Address"
                type="email"
                className="w-full p-3 rounded-lg border border-app-border bg-app-bg focus:ring-2 focus:ring-app-accent outline-none"
                onChange={(e) =>
                  setFormData({ ...formData, email: e.target.value })
                }
              />
              <input
                required
                placeholder="First Name"
                className="w-full p-3 rounded-lg border border-app-border bg-app-bg focus:ring-2 focus:ring-app-accent outline-none"
                onChange={(e) =>
                  setFormData({ ...formData, name: e.target.value })
                }
              />
              <input
                required
                placeholder="Surname"
                className="w-full p-3 rounded-lg border border-app-border bg-app-bg focus:ring-2 focus:ring-app-accent outline-none"
                onChange={(e) =>
                  setFormData({ ...formData, surname: e.target.value })
                }
              />
              <input
                required
                placeholder="Other Names"
                className="w-full p-3 rounded-lg border border-app-border bg-app-bg focus:ring-2 focus:ring-app-accent outline-none"
                onChange={(e) =>
                  setFormData({ ...formData, other_names: e.target.value })
                }
              />
              <input
                required
                placeholder="Program"
                className="col-span-full w-full p-3 rounded-lg border border-app-border bg-app-bg focus:ring-2 focus:ring-app-accent outline-none"
                onChange={(e) =>
                  setFormData({ ...formData, program: e.target.value })
                }
              />
            </div>
            <button
              type="submit"
              className="mt-6 w-full md:w-auto bg-app-accent text-white px-8 py-3 rounded-lg font-semibold hover:opacity-90 transition"
            >
              Submit
            </button>
          </form>
        </div>
      )}

      <div className="bg-app-bg rounded-xl border border-app-border overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-app-bg border-b border-app-border">
            <tr>
              <th className="p-4 text-app-text-h font-semibold">Name</th>
              <th className="p-4 text-app-text-h font-semibold">Email</th>
              <th className="p-4 text-app-text-h font-semibold">Program</th>
              <th className="p-4 text-app-text-h font-semibold">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-app-border">
            {subscribers.map((sub) => (
              <tr
                key={sub.email}
                className="hover:bg-app-border/10 transition-colors"
              >
                <td className="p-4 text-app-text">{`${sub.name} ${sub.other_names} ${sub.surname}`}</td>
                <td className="p-4 text-app-text">{sub.email}</td>
                <td className="p-4 text-app-text">{sub.program}</td>
                <td className="p-4">
                  <button
                    onClick={() => handleDelete(sub.email)}
                    className="text-red-500 hover:underline font-medium text-sm"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

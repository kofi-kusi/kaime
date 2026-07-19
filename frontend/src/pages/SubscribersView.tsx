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
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Subscribers</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-600 text-white px-4 py-2 rounded shadow"
        >
          {showForm ? "Cancel" : "Add Subscriber"}
        </button>
      </div>

      {showForm && (
        <form
          onSubmit={handleCreate}
          className="bg-white p-6 rounded shadow mb-6 border"
        >
          <div className="grid grid-cols-2 gap-4">
            <input
              required
              placeholder="Email"
              type="email"
              className="border p-2 rounded"
              onChange={(e) =>
                setFormData({ ...formData, email: e.target.value })
              }
            />
            <input
              required
              placeholder="First Name"
              className="border p-2 rounded"
              onChange={(e) =>
                setFormData({ ...formData, name: e.target.value })
              }
            />
            <input
              required
              placeholder="Surname"
              className="border p-2 rounded"
              onChange={(e) =>
                setFormData({ ...formData, surname: e.target.value })
              }
            />
            <input
              required
              placeholder="Other Names"
              className="border p-2 rounded"
              onChange={(e) =>
                setFormData({ ...formData, other_names: e.target.value })
              }
            />
            <input
              required
              placeholder="Program"
              className="border p-2 rounded"
              onChange={(e) =>
                setFormData({ ...formData, program: e.target.value })
              }
            />
          </div>
          <button
            type="submit"
            className="mt-4 bg-green-600 text-white px-4 py-2 rounded"
          >
            Submit
          </button>
        </form>
      )}

      <div className="bg-white rounded shadow overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-gray-100 border-b">
              <th className="p-3">Name</th>
              <th className="p-3">Email</th>
              <th className="p-3">Program</th>
              <th className="p-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            {subscribers.map((sub) => (
              <tr key={sub.email} className="border-b">
                <td className="p-3">{`${sub.name} ${sub.other_names} ${sub.surname}`}</td>
                <td className="p-3">{sub.email}</td>
                <td className="p-3">{sub.program}</td>
                <td className="p-3">
                  <button
                    onClick={() => handleDelete(sub.email)}
                    className="text-red-600 hover:underline"
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

import React, { useState, useEffect } from "react";
import { api, type Event, type EventCreate, EventEmailTemplate } from "../api";

export default function EventsView() {
  const [events, setEvents] = useState<Event[]>([]);
  const [showForm, setShowForm] = useState(false);

  // Form State
  const [formData, setFormData] = useState<Partial<EventCreate>>({
    email_template: EventEmailTemplate.EVENT_REMINDER,
    is_active: true,
  });
  const [offsetsInput, setOffsetsInput] = useState("");

  const loadEvents = async () => {
    const data = await api.getEvents();
    setEvents(data);
  };

  useEffect(() => {
    loadEvents();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload = {
        ...formData,
        notification_offsets: offsetsInput
          ? offsetsInput.split(",").map((n) => parseInt(n.trim(), 10))
          : undefined,
      } as EventCreate;
      console.log(payload);
      await api.createEvent(payload);
      setShowForm(false);
      loadEvents();
    } catch (error) {
      alert(`Error creating event: ${error}`);
    }
  };

  const toggleStatus = async (id: number, currentStatus: boolean) => {
    await api.toggleEventStatus(id, !currentStatus);
    loadEvents();
  };

  const handleDelete = async (id: number) => {
    if (window.confirm("Delete this event?")) {
      await api.deleteEvent(id);
      loadEvents();
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-app-text-h">Events</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-app-accent text-white px-5 py-2 rounded-lg font-medium hover:opacity-90 transition shadow-sm"
        >
          {showForm ? "Cancel" : "Create Event"}
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
                placeholder="Event Title"
                className="col-span-full w-full p-3 rounded-lg border border-app-border bg-app-bg focus:ring-2 focus:ring-app-accent outline-none"
                onChange={(e) =>
                  setFormData({ ...formData, title: e.target.value })
                }
              />

              <div className="flex flex-col gap-1">
                <label className="text-sm font-medium text-app-text">
                  Start Date
                </label>
                <input
                  type="datetime-local"
                  required
                  className="w-full p-3 rounded-lg border border-app-border bg-app-bg focus:ring-2 focus:ring-app-accent outline-none"
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      start_date: new Date(e.target.value).toISOString(),
                    })
                  }
                />
              </div>

              <div className="flex flex-col gap-1">
                <label className="text-sm font-medium text-app-text">
                  End Date
                </label>
                <input
                  type="datetime-local"
                  className="w-full p-3 rounded-lg border border-app-border bg-app-bg focus:ring-2 focus:ring-app-accent outline-none"
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      end_date: new Date(e.target.value).toISOString(),
                    })
                  }
                />
              </div>

              <input
                type="number"
                placeholder="Days Before Notification"
                className="w-full p-3 rounded-lg border border-app-border bg-app-bg focus:ring-2 focus:ring-app-accent outline-none"
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    notification_days_before: parseInt(e.target.value),
                  })
                }
              />

              <input
                placeholder="Offsets (e.g. 1,3,7)"
                className="w-full p-3 rounded-lg border border-app-border bg-app-bg focus:ring-2 focus:ring-app-accent outline-none"
                value={offsetsInput}
                onChange={(e) => setOffsetsInput(e.target.value)}
              />

              <select
                className="w-full p-3 rounded-lg border border-app-border bg-app-bg focus:ring-2 focus:ring-app-accent outline-none"
                value={formData.email_template}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    email_template: e.target.value as EventEmailTemplate,
                  })
                }
              >
                {Object.values(EventEmailTemplate).map((tpl) => (
                  <option key={tpl} value={tpl}>
                    {tpl}
                  </option>
                ))}
              </select>

              <textarea
                required
                placeholder="Event Description"
                rows={4}
                className="col-span-full w-full p-3 rounded-lg border border-app-border bg-app-bg focus:ring-2 focus:ring-app-accent outline-none"
                onChange={(e) =>
                  setFormData({ ...formData, body: e.target.value })
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
              <th className="p-4 text-app-text-h font-semibold">Title</th>
              <th className="p-4 text-app-text-h font-semibold">Start Date</th>
              <th className="p-4 text-app-text-h font-semibold">Template</th>
              <th className="p-4 text-app-text-h font-semibold">Status</th>
              <th className="p-4 text-app-text-h font-semibold">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-app-border">
            {events.map((event) => (
              <tr
                key={event.id}
                className="hover:bg-app-border/10 transition-colors"
              >
                <td className="p-4 text-app-text">{event.title}</td>
                <td className="p-4 text-app-text">
                  {new Date(event.start_date).toLocaleDateString()}
                </td>
                <td className="p-4 text-app-text text-sm">
                  {event.email_template}
                </td>
                <td className="p-4">
                  <span
                    className={`px-2 py-1 rounded-full text-xs font-medium ${event.is_active ? "bg-green-500/10 text-green-600" : "bg-red-500/10 text-red-600"}`}
                  >
                    {event.is_active ? "Active" : "Inactive"}
                  </span>
                </td>
                <td className="p-4 space-x-3">
                  <button
                    onClick={() => toggleStatus(event.id, event.is_active)}
                    className="text-app-accent hover:underline font-medium text-sm"
                  >
                    Toggle
                  </button>
                  <button
                    onClick={() => handleDelete(event.id)}
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

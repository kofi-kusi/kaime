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
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Events</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-600 text-white px-4 py-2 rounded shadow"
        >
          {showForm ? "Cancel" : "Create Event"}
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
              placeholder="Title"
              className="border p-2 rounded col-span-full"
              onChange={(e) =>
                setFormData({ ...formData, title: e.target.value })
              }
            />

            <div className="flex flex-col">
              <label className="text-sm text-gray-600">Start Date</label>
              <input
                type="datetime-local"
                required
                className="border p-2 rounded"
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    start_date: new Date(e.target.value).toISOString(),
                  })
                }
              />
            </div>

            <div className="flex flex-col">
              <label className="text-sm text-gray-600">End Date</label>
              <input
                type="datetime-local"
                className="border p-2 rounded"
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
              placeholder="Notification Days Before"
              className="border p-2 rounded"
              onChange={(e) =>
                setFormData({
                  ...formData,
                  notification_days_before: parseInt(e.target.value),
                })
              }
            />

            <input
              placeholder="Offsets (comma separated, e.g., 1,3,7)"
              className="border p-2 rounded"
              value={offsetsInput}
              onChange={(e) => setOffsetsInput(e.target.value)}
            />

            <select
              className="border p-2 rounded"
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
              placeholder="body"
              rows={5}
              className="border p-2 rounded col-span-full"
              onChange={(e) =>
                setFormData({ ...formData, body: e.target.value })
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
              <th className="p-3">Title</th>
              <th className="p-3">Start Date</th>
              <th className="p-3">Template</th>
              <th className="p-3">Status</th>
              <th className="p-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            {events.map((event) => (
              <tr key={event.id} className="border-b">
                <td className="p-3">{event.title}</td>
                <td className="p-3">
                  {new Date(event.start_date).toLocaleDateString()}
                </td>
                <td className="p-3">{event.email_template}</td>
                <td className="p-3">
                  <span
                    className={`px-2 py-1 rounded text-xs text-white ${event.is_active ? "bg-green-500" : "bg-red-500"}`}
                  >
                    {event.is_active ? "Active" : "Inactive"}
                  </span>
                </td>
                <td className="p-3 space-x-2">
                  <button
                    onClick={() => toggleStatus(event.id, event.is_active)}
                    className="text-blue-600 hover:underline"
                  >
                    Toggle Status
                  </button>
                  <button
                    onClick={() => handleDelete(event.id)}
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

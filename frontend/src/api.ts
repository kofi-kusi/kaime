export const EventEmailTemplate = {
  ANNOUNCEMENT: "announcement.html",
  DEADLINE_REMINDER: "deadline_reminder.html",
  EVENT_REMINDER: "event_reminder.html",
  EXAM_REMINDER: "exam_reminder.html",
  REGISTRATION_CLOSING: "registration_closing.html",
  REGISTRATION_OPEN: "registration_open.html",
  REGISTRATION_REMINDER: "registration_reminder.html",
  RESULTS_PUBLISHED: "results_published.html",
  RESULTS_PUBLISHED_REMINDER: "results_published_reminder.html",
  UPCOMING_EVENT_REMINDER: "upcoming_event_reminder.html",
  VAC_RE_OPENING_REMINDER: "vac-re-opening_reminder.html",
} as const;

// This extracts the values into a reusable TypeScript type
export type EventEmailTemplate =
  (typeof EventEmailTemplate)[keyof typeof EventEmailTemplate];

export interface Subscriber {
  email: string;
  name: string;
  program: string;
  surname: string;
  other_names: string;
}

export interface Event {
  id: number;
  title: string;
  body: string;
  start_date: string;
  end_date?: string;
  notification_days_before?: number;
  notification_offsets?: number[];
  email_template: EventEmailTemplate;
  is_active: boolean;
}

export type EventCreate = Omit<Event, "id">;

// --- API Client ---
const API_BASE = "/";

export const api = {
  // Subscribers
  getSubscribers: async (): Promise<Subscriber[]> => {
    const res = await fetch(`${API_BASE}dashboard/subscribers`);
    return res.json();
  },
  createSubscriber: async (data: Subscriber): Promise<Subscriber> => {
    const res = await fetch(`${API_BASE}dashboard/subscribers`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Failed to create subscriber");
    return res.json();
  },
  deleteSubscriber: async (email: string): Promise<void> => {
    await fetch(`${API_BASE}dashboard/subscribers/${email}`, { method: "DELETE" });
  },

  // Events
  getEvents: async (): Promise<Event[]> => {
    const res = await fetch(`${API_BASE}dashboard/events`);
    return res.json();
  },
  createEvent: async (data: EventCreate): Promise<Event> => {
    const res = await fetch(`${API_BASE}dashboard/events`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Failed to create event");
    return res.json();
  },
  toggleEventStatus: async (id: number, activate: boolean): Promise<Event> => {
    const action = activate ? "activate" : "deactivate";
    const res = await fetch(`${API_BASE}dashboard/events/${id}/${action}`, {
      method: "PATCH",
    });
    return res.json();
  },
  deleteEvent: async (id: number): Promise<void> => {
    await fetch(`${API_BASE}dashboard/events/${id}`, { method: "DELETE" });
  },
};

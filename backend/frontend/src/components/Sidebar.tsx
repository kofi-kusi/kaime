import { Link } from 'react-router'

export default function Sibebar() {
  return (
    <div className="flex flex-col">
      <Link to="/events">Events</Link>
      <Link to="/subscribers">Subscribers</Link>
    </div>
  )
}

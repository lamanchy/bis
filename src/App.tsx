import { Button } from 'antd'
import { useEffect } from 'react'
import { Route, Routes } from 'react-router-dom'
import { useAppDispatch, useAppSelector } from './app/hooks'
import CloseEvent from './features/event/CloseEvent'
import CreateEvent from './features/event/CreateEvent'
import EventList from './features/event/EventList'
import EventParticipants from './features/event/EventParticipants'
import Login from './features/login/Login'
import { chooseRole, init, selectLogin } from './features/login/loginSlice'
import RoleSwitch from './features/login/RoleSwitch'
import Footer from './Footer'
import GuidePost from './GuidePost'
import Header from './Header'

function App() {
  const { currentRole, isLoggedIn, isPending } = useAppSelector(selectLogin)
  const dispatch = useAppDispatch()
  useEffect(() => {
    dispatch(init())
  }, [dispatch])
  return (
    <>
      <div className="min-h-screen w-full">
        <Header />
        <div className="p-6">
          {isPending ? (
            <div>Přihlašování</div>
          ) : !isLoggedIn ? (
            <Login />
          ) : currentRole === '' ? (
            <RoleSwitch />
          ) : currentRole === 'org' ? (
            <Routes>
              <Route path="/" element={<GuidePost />} />
              <Route path="/events/create" element={<CreateEvent />} />
              <Route path="/events/:eventId/edit" element={<CreateEvent />} />
              <Route path="/events/:eventId/close" element={<CloseEvent />} />
              <Route
                path="/events/:eventId/participants"
                element={<EventParticipants />}
              />
              <Route path="/events" element={<EventList />} />
            </Routes>
          ) : (
            <div className="flex items-center justify-center flex-col gap-4">
              not implemented
              <Button onClick={() => dispatch(chooseRole(''))}>Back</Button>
            </div>
          )}
        </div>
        <Footer />
      </div>
    </>
  )
}

export default App

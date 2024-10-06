import React, { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Slider } from "@/components/ui/slider"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { MapPin, Calendar, Users, CheckSquare, Briefcase, Flag, Loader2, AlertCircle } from 'lucide-react'
import axios from 'axios'
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"

export default function OpportunitiesPage() {
  const [quizResults, setQuizResults] = useState([])
  const [address, setAddress] = useState('')
  const [pollingPlaces, setPollingPlaces] = useState([])
  const [civicEvents, setCivicEvents] = useState([])
  const [quizCompleted, setQuizCompleted] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const quizEvents = [
    { id: 1, name: "Local Town Hall Meeting", description: "Discuss current issues affecting our community" },
    { id: 2, name: "Community Clean-up Day", description: "Help beautify our neighborhood parks and streets" },
    { id: 3, name: "Youth Mentorship Program", description: "Guide and support local youth in their personal development" },
    { id: 4, name: "Voter Registration Drive", description: "Assist in registering new voters for upcoming elections" },
    { id: 5, name: "Local Food Bank Volunteer", description: "Sort and distribute food to those in need in our community" }
  ]

  const handleQuizSubmit = (event) => {
    event.preventDefault()
    const formData = new FormData(event.target)
    const results = quizEvents.map(quizEvent => ({
      ...quizEvent,
      rating: parseInt(formData.get(`rating-${quizEvent.id}`))
    }))
    setQuizResults(results)
    setQuizCompleted(true)
  }

  const handleAddressSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    setError('')
    setPollingPlaces([])
    setCivicEvents([])

    try {
      const response = await axios.post('/api/civic-info', { address }, {
        timeout: 10000, // 10 second timeout
      })
      console.log('API Response:', response.data) // Log the entire response for debugging

      const { election_info, polling_locations, event_info } = response.data

      if (polling_locations && polling_locations.length > 0) {
        setPollingPlaces(polling_locations)
      } else {
        console.warn('No polling locations found')
        setError('No polling locations found for the given address.')
      }

      if (event_info && event_info.length > 0) {
        setCivicEvents(event_info)
      } else {
        console.warn('No civic events found')
        // We don't set an error here as it's not critical
      }

    } catch (err) {
      console.error('Error fetching civic information:', err)
      if (err.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.error('Error response:', err.response.data)
        console.error('Error status:', err.response.status)
        setError(`Server error: ${err.response.status}. Please try again later.`)
      } else if (err.request) {
        // The request was made but no response was received
        console.error('No response received:', err.request)
        setError('No response from server. Please check your internet connection and try again.')
      } else {
        // Something happened in setting up the request that triggered an Error
        console.error('Error message:', err.message)
        setError('An unexpected error occurred. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white dark:from-gray-900 dark:to-gray-800">
      <header className="bg-blue-600 text-white shadow">
        <nav className="container mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-2">
              <Flag className="h-8 w-8" />
              <div className="text-2xl font-bold">Civix</div>
            </div>
            <div className="flex space-x-4">
              <Button variant="ghost" className="text-white hover:text-blue-200">Home</Button>
              <Button variant="ghost" className="text-white hover:text-blue-200">Opportunities</Button>
              <Button variant="ghost" className="text-white hover:text-blue-200">Leaderboard</Button>
              <Button variant="ghost" className="text-white hover:text-blue-200">Profile</Button>
            </div>
          </div>
        </nav>
      </header>

      <main className="container mx-auto px-6 py-8">
        <h1 className="text-3xl font-bold mb-8 text-center text-blue-800 dark:text-blue-200">Civic Engagement Opportunities</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <Card className="bg-white dark:bg-gray-800 shadow-lg">
            <CardHeader className="bg-green-500 text-white rounded-t-lg">
              <CardTitle className="text-2xl font-bold flex items-center">
                <Users className="mr-2 h-6 w-6" />
                Event Interest Quiz
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              {!quizCompleted ? (
                <form onSubmit={handleQuizSubmit}>
                  {quizEvents.map(event => (
                    <div key={event.id} className="mb-6">
                      <h3 className="font-semibold mb-2">{event.name}</h3>
                      <p className="text-sm text-gray-600 dark:text-gray-300 mb-2">{event.description}</p>
                      <div className="flex items-center space-x-2">
                        <span className="text-sm">1</span>
                        <Slider
                          name={`rating-${event.id}`}
                          min={1}
                          max={10}
                          step={1}
                          defaultValue={[5]}
                        />
                        <span className="text-sm">10</span>
                      </div>
                    </div>
                  ))}
                  <Button type="submit" className="w-full">Submit Ratings</Button>
                </form>
              ) : (
                <div>
                  <h3 className="font-semibold mb-4">Your Event Preferences:</h3>
                  <ScrollArea className="h-[300px]">
                    {quizResults.sort((a, b) => b.rating - a.rating).map(result => (
                      <div key={result.id} className="mb-4 p-3 bg-blue-50 dark:bg-blue-900 rounded-lg">
                        <div className="flex justify-between items-center">
                          <span className="font-medium">{result.name}</span>
                          <Badge variant="secondary">{result.rating}/10</Badge>
                        </div>
                        <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">{result.description}</p>
                      </div>
                    ))}
                  </ScrollArea>
                </div>
              )}
            </CardContent>
          </Card>

          <Card className="bg-white dark:bg-gray-800 shadow-lg">
            <CardHeader className="bg-blue-500 text-white rounded-t-lg">
              <CardTitle className="text-2xl font-bold flex items-center">
                <MapPin className="mr-2 h-6 w-6" />
                Find Polling Places
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <form onSubmit={handleAddressSubmit} className="mb-6">
                <div className="flex space-x-2">
                  <Input
                    placeholder="Enter your address"
                    value={address}
                    onChange={(e) => setAddress(e.target.value)}
                    className="flex-grow"
                  />
                  <Button type="submit" disabled={loading}>
                    {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : 'Find'}
                  </Button>
                </div>
              </form>
              {error && (
                <Alert variant="destructive" className="mb-4">
                  <AlertCircle className="h-4 w-4" />
                  <AlertTitle>Error</AlertTitle>
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}
              {pollingPlaces.length > 0 && (
                <div>
                  <h3 className="font-semibold mb-4">Nearby Polling Places:</h3>
                  <ScrollArea className="h-[200px]">
                    {pollingPlaces.map((place, index) => (
                      <div key={index} className="mb-4 p-3 bg-blue-50 dark:bg-blue-900 rounded-lg">
                        <div className="font-medium">{place.address.locationName}</div>
                        <div className="text-sm text-gray-600 dark:text-gray-300">{place.address.line1}</div>
                      </div>
                    ))}
                  </ScrollArea>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        <Card className="mt-8 bg-white dark:bg-gray-800 shadow-lg">
          <CardHeader className="bg-yellow-500 text-white rounded-t-lg">
            <CardTitle className="text-2xl font-bold flex items-center">
              <Calendar className="mr-2 h-6 w-6" />
              Upcoming Civic Opportunities
            </CardTitle>
          </CardHeader>
          <CardContent className="p-6">
            {civicEvents.length > 0 ? (
              <ScrollArea className="h-[300px]">
                {civicEvents.map((event, index) => (
                  <div key={index} className="mb-4 p-4 bg-yellow-50 dark:bg-yellow-900 rounded-lg">
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="font-semibold">{event.name}</h3>
                        <p className="text-sm text-gray-600 dark:text-gray-300">
                          Lat: {event.latitude}, Long: {event.longitude}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </ScrollArea>
            ) : (
              <p className="text-center text-gray-500">No upcoming events found. Try searching for a different address.</p>
            )}
          </CardContent>
        </Card>
      </main>

      <footer className="bg-blue-600 text-white mt-12">
        <div className="container mx-auto px-6 py-4">
          <p className="text-center">
            © 2024 Civix. Empowering civic engagement through technology.
          </p>
        </div>
      </footer>
    </div>
  )
}
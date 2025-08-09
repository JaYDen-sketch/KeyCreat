import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Gamepad2, Play, Key, Star, Shield, Zap, Users, Crown, Check, ShoppingCart, Tag, X, User, Lock } from 'lucide-react'
import './App.css'

// Import images
import heroController from './assets/SKoWXOkKDupe.jpg'
import steamKeys from './assets/YDkNDU7ePFkG.jpg'
import ottServices from './assets/zeWluOqpfFRD.webp'
import gamingSetup from './assets/FsfW7CoqrmPE.jpg'

function App() {
  const [email, setEmail] = useState('')
  const [showLoginModal, setShowLoginModal] = useState(false)
  const [showRegisterModal, setShowRegisterModal] = useState(false)
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [user, setUser] = useState(null)
  const [loginForm, setLoginForm] = useState({ username: '', password: '' })
  const [registerForm, setRegisterForm] = useState({ 
    username: '', 
    email: '', 
    password: '', 
    confirmPassword: '',
    firstName: '',
    lastName: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // API Base URL
  const API_BASE = '/api'

  // Login function
  const handleLogin = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: loginForm.username,
          password: loginForm.password
        }),
        credentials: 'include'
      })

      const data = await response.json()

      if (response.ok) {
        setIsLoggedIn(true)
        setUser(data.user)
        setShowLoginModal(false)
        setLoginForm({ username: '', password: '' })
        alert('Login successful!')
      } else {
        setError(data.error || 'Login failed')
      }
    } catch (error) {
      setError('Network error. Please try again.')
      console.error('Login error:', error)
    } finally {
      setLoading(false)
    }
  }

  // Register function
  const handleRegister = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    if (registerForm.password !== registerForm.confirmPassword) {
      setError('Passwords do not match')
      setLoading(false)
      return
    }

    try {
      const response = await fetch(`${API_BASE}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: registerForm.username,
          email: registerForm.email,
          password: registerForm.password,
          first_name: registerForm.firstName,
          last_name: registerForm.lastName
        }),
        credentials: 'include'
      })

      const data = await response.json()

      if (response.ok) {
        setShowRegisterModal(false)
        setShowLoginModal(true)
        setRegisterForm({ 
          username: '', 
          email: '', 
          password: '', 
          confirmPassword: '',
          firstName: '',
          lastName: ''
        })
        alert('Registration successful! Please log in.')
      } else {
        setError(data.error || 'Registration failed')
      }
    } catch (error) {
      setError('Network error. Please try again.')
      console.error('Registration error:', error)
    } finally {
      setLoading(false)
    }
  }

  // Logout function
  const handleLogout = async () => {
    try {
      await fetch(`${API_BASE}/auth/logout`, {
        method: 'POST',
        credentials: 'include'
      })
      setIsLoggedIn(false)
      setUser(null)
      alert('Logged out successfully!')
    } catch (error) {
      console.error('Logout error:', error)
    }
  }

  const services = [
    {
      icon: <Gamepad2 className="h-12 w-12 text-primary" />,
      title: "Game Subscriptions",
      description: "Access to premium gaming platforms including Xbox Game Pass, PlayStation Plus, and more",
      image: heroController,
      features: ["100+ Premium Games", "Day-1 Releases", "Cloud Gaming", "Cross-Platform"]
    },
    {
      icon: <Play className="h-12 w-12 text-accent" />,
      title: "OTT Streaming",
      description: "Premium streaming services for movies, TV shows, and exclusive gaming content",
      image: ottServices,
      features: ["4K Streaming", "Multiple Devices", "Offline Downloads", "Exclusive Content"]
    },
    {
      icon: <Key className="h-12 w-12 text-chart-3" />,
      title: "Steam Keys",
      description: "Instant delivery of genuine Steam keys for the latest and greatest games",
      image: steamKeys,
      features: ["Instant Delivery", "Genuine Keys", "Latest Releases", "Bulk Discounts"]
    }
  ]

  const steamKeyCategories = [
    {
      category: "AAA Action Games",
      games: [
        { name: "Call of Duty: Modern Warfare III", price: "$59.99", originalPrice: "$69.99", discount: "14%" },
        { name: "Cyberpunk 2077", price: "$29.99", originalPrice: "$59.99", discount: "50%" },
        { name: "Grand Theft Auto V", price: "$19.99", originalPrice: "$29.99", discount: "33%" },
        { name: "Red Dead Redemption 2", price: "$39.99", originalPrice: "$59.99", discount: "33%" }
      ]
    },
    {
      category: "Indie & Strategy",
      games: [
        { name: "Hades", price: "$14.99", originalPrice: "$24.99", discount: "40%" },
        { name: "Civilization VI", price: "$19.99", originalPrice: "$59.99", discount: "67%" },
        { name: "Stardew Valley", price: "$9.99", originalPrice: "$14.99", discount: "33%" },
        { name: "Among Us", price: "$2.99", originalPrice: "$4.99", discount: "40%" }
      ]
    },
    {
      category: "Racing & Sports",
      games: [
        { name: "Forza Horizon 5", price: "$39.99", originalPrice: "$59.99", discount: "33%" },
        { name: "FIFA 24", price: "$49.99", originalPrice: "$69.99", discount: "29%" },
        { name: "F1 24", price: "$44.99", originalPrice: "$69.99", discount: "36%" },
        { name: "NBA 2K24", price: "$29.99", originalPrice: "$59.99", discount: "50%" }
      ]
    },
    {
      category: "Horror & Survival",
      games: [
        { name: "Resident Evil 4 Remake", price: "$39.99", originalPrice: "$59.99", discount: "33%" },
        { name: "Dead by Daylight", price: "$9.99", originalPrice: "$19.99", discount: "50%" },
        { name: "Phasmophobia", price: "$8.99", originalPrice: "$13.99", discount: "36%" },
        { name: "The Forest", price: "$12.99", originalPrice: "$19.99", discount: "35%" }
      ]
    }
  ]

  const ottServiceCategories = [
    {
      category: "Video Streaming",
      services: [
        { name: "Netflix Premium", price: "$8.99", originalPrice: "$15.99", discount: "44%", duration: "1 Month" },
        { name: "Amazon Prime Video", price: "$6.99", originalPrice: "$8.99", discount: "22%", duration: "1 Month" },
        { name: "Disney+ Premium", price: "$7.99", originalPrice: "$10.99", discount: "27%", duration: "1 Month" },
        { name: "HBO Max", price: "$9.99", originalPrice: "$14.99", discount: "33%", duration: "1 Month" }
      ]
    },
    {
      category: "Music Streaming",
      services: [
        { name: "Spotify Premium", price: "$4.99", originalPrice: "$9.99", discount: "50%", duration: "1 Month" },
        { name: "Apple Music", price: "$5.99", originalPrice: "$9.99", discount: "40%", duration: "1 Month" },
        { name: "YouTube Music Premium", price: "$4.99", originalPrice: "$9.99", discount: "50%", duration: "1 Month" },
        { name: "Amazon Music Unlimited", price: "$5.99", originalPrice: "$8.99", discount: "33%", duration: "1 Month" }
      ]
    },
    {
      category: "Gaming Subscriptions",
      services: [
        { name: "Xbox Game Pass Ultimate", price: "$12.99", originalPrice: "$16.99", discount: "24%", duration: "1 Month" },
        { name: "PlayStation Plus Premium", price: "$14.99", originalPrice: "$17.99", discount: "17%", duration: "1 Month" },
        { name: "EA Play Pro", price: "$9.99", originalPrice: "$14.99", discount: "33%", duration: "1 Month" },
        { name: "Ubisoft+", price: "$11.99", originalPrice: "$14.99", discount: "20%", duration: "1 Month" }
      ]
    },
    {
      category: "Anime & Entertainment",
      services: [
        { name: "Crunchyroll Premium", price: "$6.99", originalPrice: "$9.99", discount: "30%", duration: "1 Month" },
        { name: "Funimation Premium", price: "$5.99", originalPrice: "$7.99", discount: "25%", duration: "1 Month" },
        { name: "VRV Premium", price: "$7.99", originalPrice: "$9.99", discount: "20%", duration: "1 Month" },
        { name: "Hulu (No Ads)", price: "$8.99", originalPrice: "$11.99", discount: "25%", duration: "1 Month" }
      ]
    }
  ]

  const plans = [
    {
      name: "Starter",
      price: "$9.99",
      period: "/month",
      description: "Perfect for casual gamers",
      features: [
        "5 Game Downloads",
        "Basic OTT Access",
        "Standard Support",
        "Mobile Gaming"
      ],
      popular: false
    },
    {
      name: "Pro Gamer",
      price: "$19.99",
      period: "/month",
      description: "For serious gaming enthusiasts",
      features: [
        "Unlimited Game Downloads",
        "Premium OTT Services",
        "Priority Support",
        "Cloud Gaming",
        "Early Access",
        "Steam Key Discounts"
      ],
      popular: true
    },
    {
      name: "Ultimate",
      price: "$29.99",
      period: "/month",
      description: "The complete gaming experience",
      features: [
        "Everything in Pro",
        "Exclusive Beta Access",
        "VIP Support",
        "Custom Game Requests",
        "Free Steam Keys",
        "Gaming Hardware Discounts"
      ],
      popular: false
    }
  ]

  const testimonials = [
    {
      name: "Alex Chen",
      rating: 5,
      comment: "GameVault has revolutionized my gaming experience. The variety of games and instant access is incredible!"
    },
    {
      name: "Sarah Johnson",
      rating: 5,
      comment: "Best value for money! I've saved hundreds on games and streaming services."
    },
    {
      name: "Mike Rodriguez",
      rating: 5,
      comment: "The Steam key delivery is lightning fast, and the customer support is top-notch."
    }
  ]

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Gamepad2 className="h-8 w-8 text-primary" />
            <span className="text-2xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              GameVault
            </span>
          </div>
          <nav className="hidden md:flex items-center space-x-6">
            <a href="#services" className="text-muted-foreground hover:text-foreground transition-colors">Services</a>
            <a href="#pricing" className="text-muted-foreground hover:text-foreground transition-colors">Pricing</a>
            <a href="#testimonials" className="text-muted-foreground hover:text-foreground transition-colors">Reviews</a>
            <a href="#contact" className="text-muted-foreground hover:text-foreground transition-colors">Contact</a>
          </nav>
          <div className="flex items-center space-x-4">
            {isLoggedIn ? (
              <div className="flex items-center space-x-4">
                <span className="hidden md:inline-flex text-sm text-muted-foreground">
                  Welcome, {user?.first_name || user?.username}!
                </span>
                <Button variant="ghost" onClick={handleLogout} className="hidden md:inline-flex">
                  Logout
                </Button>
              </div>
            ) : (
              <>
                <Button variant="ghost" onClick={() => setShowLoginModal(true)} className="hidden md:inline-flex">
                  Sign In
                </Button>
                <Button onClick={() => setShowRegisterModal(true)} className="bg-primary hover:bg-primary/90">
                  Get Started
                </Button>
              </>
            )}
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative py-20 lg:py-32 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/20 via-background to-accent/20"></div>
        <div className="container mx-auto px-4 relative z-10">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-8">
              <div className="space-y-4">
                <Badge className="bg-primary/20 text-primary border-primary/30">
                  <Zap className="h-4 w-4 mr-1" />
                  Premium Gaming Access
                </Badge>
                <h1 className="text-4xl lg:text-6xl font-bold leading-tight">
                  Unlock the Ultimate
                  <span className="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent block">
                    Gaming Experience
                  </span>
                </h1>
                <p className="text-xl text-muted-foreground leading-relaxed">
                  Access premium game subscriptions, OTT streaming services, and instant Steam keys all in one place. 
                  Join thousands of gamers who trust GameVault for their digital entertainment needs.
                </p>
              </div>
              <div className="flex flex-col sm:flex-row gap-4">
                <Button size="lg" className="bg-primary hover:bg-primary/90 text-primary-foreground">
                  <Crown className="h-5 w-5 mr-2" />
                  Start Free Trial
                </Button>
                <Button size="lg" variant="outline" className="border-primary text-primary hover:bg-primary/10">
                  View Plans
                </Button>
              </div>
              <div className="flex items-center space-x-8 text-sm text-muted-foreground">
                <div className="flex items-center space-x-2">
                  <Shield className="h-5 w-5 text-green-500" />
                  <span>Secure & Trusted</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Users className="h-5 w-5 text-blue-500" />
                  <span>50K+ Users</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Star className="h-5 w-5 text-yellow-500" />
                  <span>4.9/5 Rating</span>
                </div>
              </div>
            </div>
            <div className="relative">
              <div className="relative rounded-2xl overflow-hidden shadow-2xl">
                <img 
                  src={heroController} 
                  alt="Gaming Controller" 
                  className="w-full h-auto object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-background/80 via-transparent to-transparent"></div>
              </div>
              <div className="absolute -bottom-6 -right-6 bg-card border border-border rounded-xl p-4 shadow-lg">
                <div className="flex items-center space-x-3">
                  <div className="h-3 w-3 bg-green-500 rounded-full animate-pulse"></div>
                  <span className="text-sm font-medium">Live Gaming Sessions: 12,847</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section id="services" className="py-20 bg-card/30">
        <div className="container mx-auto px-4">
          <div className="text-center space-y-4 mb-16">
            <Badge className="bg-accent/20 text-accent border-accent/30">Our Services</Badge>
            <h2 className="text-3xl lg:text-5xl font-bold">Everything You Need for Gaming</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              From the latest games to premium streaming content, we've got your digital entertainment covered.
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            {services.map((service, index) => (
              <Card key={index} className="group hover:shadow-xl transition-all duration-300 hover:-translate-y-2 bg-card border-border">
                <CardHeader className="text-center">
                  <div className="mx-auto mb-4 p-3 bg-primary/10 rounded-full w-fit group-hover:scale-110 transition-transform">
                    {service.icon}
                  </div>
                  <CardTitle className="text-xl">{service.title}</CardTitle>
                  <CardDescription className="text-muted-foreground">
                    {service.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="relative rounded-lg overflow-hidden mb-4">
                    <img 
                      src={service.image} 
                      alt={service.title}
                      className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                  </div>
                  <ul className="space-y-2">
                    {service.features.map((feature, idx) => (
                      <li key={idx} className="flex items-center space-x-2 text-sm">
                        <Check className="h-4 w-4 text-green-500" />
                        <span>{feature}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
                <CardFooter>
                  <Button className="w-full" variant="outline">
                    Learn More
                  </Button>
                </CardFooter>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Steam Keys Marketplace Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="text-center space-y-4 mb-16">
            <Badge className="bg-chart-3/20 text-chart-3 border-chart-3/30">
              <Key className="h-4 w-4 mr-1" />
              Steam Keys Marketplace
            </Badge>
            <h2 className="text-3xl lg:text-5xl font-bold">Browse Games by Category</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Discover amazing deals on Steam keys across all your favorite game categories. Instant delivery guaranteed!
            </p>
          </div>
          
          <div className="space-y-12">
            {steamKeyCategories.map((category, categoryIndex) => (
              <div key={categoryIndex} className="space-y-6">
                <div className="flex items-center space-x-3">
                  <Tag className="h-6 w-6 text-primary" />
                  <h3 className="text-2xl font-bold">{category.category}</h3>
                </div>
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {category.games.map((game, gameIndex) => (
                    <Card key={gameIndex} className="group hover:shadow-xl transition-all duration-300 hover:-translate-y-1 bg-card border-border">
                      <CardHeader className="pb-3">
                        <div className="flex items-start justify-between">
                          <Badge variant="secondary" className="bg-green-500/20 text-green-400 border-green-500/30">
                            -{game.discount}
                          </Badge>
                          <Key className="h-5 w-5 text-muted-foreground" />
                        </div>
                        <CardTitle className="text-lg leading-tight">{game.name}</CardTitle>
                      </CardHeader>
                      <CardContent className="pt-0">
                        <div className="space-y-3">
                          <div className="flex items-center space-x-2">
                            <span className="text-2xl font-bold text-primary">{game.price}</span>
                            <span className="text-sm text-muted-foreground line-through">{game.originalPrice}</span>
                          </div>
                          <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                            <Shield className="h-4 w-4 text-green-500" />
                            <span>Instant Delivery</span>
                          </div>
                        </div>
                      </CardContent>
                      <CardFooter className="pt-0">
                        <Button className="w-full group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                          <ShoppingCart className="h-4 w-4 mr-2" />
                          Buy Now
                        </Button>
                      </CardFooter>
                    </Card>
                  ))}
                </div>
              </div>
            ))}
          </div>
          
          <div className="text-center mt-12">
            <Button size="lg" variant="outline" className="border-primary text-primary hover:bg-primary/10">
              View All Steam Keys
            </Button>
          </div>
        </div>
      </section>

      {/* OTT Services Marketplace Section */}
      <section className="py-20 bg-card/30">
        <div className="container mx-auto px-4">
          <div className="text-center space-y-4 mb-16">
            <Badge className="bg-accent/20 text-accent border-accent/30">
              <Play className="h-4 w-4 mr-1" />
              OTT Services Marketplace
            </Badge>
            <h2 className="text-3xl lg:text-5xl font-bold">Premium Streaming Services</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Get instant access to premium streaming subscriptions at unbeatable prices. All accounts are genuine and delivered instantly!
            </p>
          </div>
          
          <div className="space-y-12">
            {ottServiceCategories.map((category, categoryIndex) => (
              <div key={categoryIndex} className="space-y-6">
                <div className="flex items-center space-x-3">
                  <Play className="h-6 w-6 text-accent" />
                  <h3 className="text-2xl font-bold">{category.category}</h3>
                </div>
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {category.services.map((service, serviceIndex) => (
                    <Card key={serviceIndex} className="group hover:shadow-xl transition-all duration-300 hover:-translate-y-1 bg-card border-border">
                      <CardHeader className="pb-3">
                        <div className="flex items-start justify-between">
                          <Badge variant="secondary" className="bg-blue-500/20 text-blue-400 border-blue-500/30">
                            -{service.discount}
                          </Badge>
                          <Play className="h-5 w-5 text-muted-foreground" />
                        </div>
                        <CardTitle className="text-lg leading-tight">{service.name}</CardTitle>
                      </CardHeader>
                      <CardContent className="pt-0">
                        <div className="space-y-3">
                          <div className="flex items-center space-x-2">
                            <span className="text-2xl font-bold text-accent">{service.price}</span>
                            <span className="text-sm text-muted-foreground line-through">{service.originalPrice}</span>
                          </div>
                          <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                            <Shield className="h-4 w-4 text-green-500" />
                            <span>{service.duration} Access</span>
                          </div>
                        </div>
                      </CardContent>
                      <CardFooter className="pt-0">
                        <Button className="w-full group-hover:bg-accent group-hover:text-accent-foreground transition-colors">
                          <ShoppingCart className="h-4 w-4 mr-2" />
                          Subscribe Now
                        </Button>
                      </CardFooter>
                    </Card>
                  ))}
                </div>
              </div>
            ))}
          </div>
          
          <div className="text-center mt-12">
            <Button size="lg" variant="outline" className="border-accent text-accent hover:bg-accent/10">
              View All OTT Services
            </Button>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20">
        <div className="container mx-auto px-4">
          <div className="text-center space-y-4 mb-16">
            <Badge className="bg-primary/20 text-primary border-primary/30">Pricing Plans</Badge>
            <h2 className="text-3xl lg:text-5xl font-bold">Choose Your Gaming Journey</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Flexible plans designed for every type of gamer. Start free and upgrade anytime.
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {plans.map((plan, index) => (
              <Card key={index} className={`relative ${plan.popular ? 'border-primary shadow-xl scale-105' : 'border-border'} bg-card`}>
                {plan.popular && (
                  <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                    <Badge className="bg-primary text-primary-foreground">Most Popular</Badge>
                  </div>
                )}
                <CardHeader className="text-center">
                  <CardTitle className="text-2xl">{plan.name}</CardTitle>
                  <CardDescription>{plan.description}</CardDescription>
                  <div className="mt-4">
                    <span className="text-4xl font-bold">{plan.price}</span>
                    <span className="text-muted-foreground">{plan.period}</span>
                  </div>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-3">
                    {plan.features.map((feature, idx) => (
                      <li key={idx} className="flex items-center space-x-2">
                        <Check className="h-4 w-4 text-green-500" />
                        <span className="text-sm">{feature}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
                <CardFooter>
                  <Button 
                    className={`w-full ${plan.popular ? 'bg-primary hover:bg-primary/90' : ''}`}
                    variant={plan.popular ? 'default' : 'outline'}
                  >
                    {plan.popular ? 'Get Started' : 'Choose Plan'}
                  </Button>
                </CardFooter>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section id="testimonials" className="py-20 bg-card/30">
        <div className="container mx-auto px-4">
          <div className="text-center space-y-4 mb-16">
            <Badge className="bg-accent/20 text-accent border-accent/30">Testimonials</Badge>
            <h2 className="text-3xl lg:text-5xl font-bold">What Gamers Say</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Join thousands of satisfied gamers who have transformed their gaming experience with GameVault.
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <Card key={index} className="bg-card border-border">
                <CardContent className="pt-6">
                  <div className="flex items-center space-x-1 mb-4">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} className="h-4 w-4 fill-yellow-500 text-yellow-500" />
                    ))}
                  </div>
                  <p className="text-muted-foreground mb-4">"{testimonial.comment}"</p>
                  <div className="font-semibold">{testimonial.name}</div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section id="contact" className="py-20 bg-gradient-to-r from-primary/20 to-accent/20">
        <div className="container mx-auto px-4 text-center">
          <div className="max-w-3xl mx-auto space-y-8">
            <h2 className="text-3xl lg:text-5xl font-bold">Ready to Level Up?</h2>
            <p className="text-xl text-muted-foreground">
              Join GameVault today and get instant access to premium gaming content, exclusive deals, and more.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
              <Input 
                type="email" 
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="flex-1"
              />
              <Button className="bg-primary hover:bg-primary/90">
                Get Started
              </Button>
            </div>
            <p className="text-sm text-muted-foreground">
              Start your free trial today. No credit card required.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-card border-t border-border">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <Gamepad2 className="h-6 w-6 text-primary" />
                <span className="text-xl font-bold">GameVault</span>
              </div>
              <p className="text-muted-foreground text-sm">
                Your ultimate destination for premium gaming subscriptions, streaming services, and instant game access.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Services</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground transition-colors">Game Subscriptions</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">OTT Streaming</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Steam Keys</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Cloud Gaming</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground transition-colors">Help Center</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Contact Us</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">FAQ</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Community</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground transition-colors">About Us</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Privacy Policy</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Terms of Service</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Careers</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-border mt-8 pt-8 text-center text-sm text-muted-foreground">
            <p>&copy; 2025 GameVault. All rights reserved. Built for gamers, by gamers.</p>
          </div>
        </div>
      </footer>

      {/* Login Modal */}
      {showLoginModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-card border border-border rounded-lg p-6 w-full max-w-md">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold">Sign In to GameVault</h2>
              <Button variant="ghost" size="sm" onClick={() => setShowLoginModal(false)}>
                <X className="h-4 w-4" />
              </Button>
            </div>
            
            {error && (
              <div className="bg-red-500/10 border border-red-500/20 text-red-500 p-3 rounded-md mb-4 text-sm">
                {error}
              </div>
            )}
            
            <form onSubmit={handleLogin} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Username</label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    type="text"
                    placeholder="Enter your username"
                    value={loginForm.username}
                    onChange={(e) => setLoginForm({...loginForm, username: e.target.value})}
                    className="pl-10"
                    required
                  />
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2">Password</label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    type="password"
                    placeholder="Enter your password"
                    value={loginForm.password}
                    onChange={(e) => setLoginForm({...loginForm, password: e.target.value})}
                    className="pl-10"
                    required
                  />
                </div>
              </div>
              
              <Button type="submit" className="w-full" disabled={loading}>
                {loading ? 'Signing In...' : 'Sign In'}
              </Button>
            </form>
            
            <div className="mt-4 text-center text-sm text-muted-foreground">
              Don't have an account?{' '}
              <button 
                onClick={() => {
                  setShowLoginModal(false)
                  setShowRegisterModal(true)
                  setError('')
                }}
                className="text-primary hover:underline"
              >
                Sign up here
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Register Modal */}
      {showRegisterModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-card border border-border rounded-lg p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold">Join GameVault</h2>
              <Button variant="ghost" size="sm" onClick={() => setShowRegisterModal(false)}>
                <X className="h-4 w-4" />
              </Button>
            </div>
            
            {error && (
              <div className="bg-red-500/10 border border-red-500/20 text-red-500 p-3 rounded-md mb-4 text-sm">
                {error}
              </div>
            )}
            
            <form onSubmit={handleRegister} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">First Name</label>
                  <Input
                    type="text"
                    placeholder="First name"
                    value={registerForm.firstName}
                    onChange={(e) => setRegisterForm({...registerForm, firstName: e.target.value})}
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Last Name</label>
                  <Input
                    type="text"
                    placeholder="Last name"
                    value={registerForm.lastName}
                    onChange={(e) => setRegisterForm({...registerForm, lastName: e.target.value})}
                    required
                  />
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2">Username</label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    type="text"
                    placeholder="Choose a username"
                    value={registerForm.username}
                    onChange={(e) => setRegisterForm({...registerForm, username: e.target.value})}
                    className="pl-10"
                    required
                  />
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2">Email</label>
                <Input
                  type="email"
                  placeholder="Enter your email"
                  value={registerForm.email}
                  onChange={(e) => setRegisterForm({...registerForm, email: e.target.value})}
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2">Password</label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    type="password"
                    placeholder="Create a password"
                    value={registerForm.password}
                    onChange={(e) => setRegisterForm({...registerForm, password: e.target.value})}
                    className="pl-10"
                    required
                  />
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2">Confirm Password</label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    type="password"
                    placeholder="Confirm your password"
                    value={registerForm.confirmPassword}
                    onChange={(e) => setRegisterForm({...registerForm, confirmPassword: e.target.value})}
                    className="pl-10"
                    required
                  />
                </div>
              </div>
              
              <Button type="submit" className="w-full" disabled={loading}>
                {loading ? 'Creating Account...' : 'Create Account'}
              </Button>
            </form>
            
            <div className="mt-4 text-center text-sm text-muted-foreground">
              Already have an account?{' '}
              <button 
                onClick={() => {
                  setShowRegisterModal(false)
                  setShowLoginModal(true)
                  setError('')
                }}
                className="text-primary hover:underline"
              >
                Sign in here
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App


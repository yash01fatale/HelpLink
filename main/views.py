from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Request

def HomePage(request):
    quick_stats = [
        {"key": "contrib", "label": "Your Contributions", "value": "47", "color": "text-rose-500"},
        {"key": "people", "label": "People Helped", "value": "35", "color": "text-blue-500"},
        {"key": "chats", "label": "Active Chats", "value": "3", "color": "text-purple-500"},
        {"key": "month", "label": "This Month", "value": "+12", "color": "text-green-500"},
    ]

    recent_requests = [
        {"id": "1", "title": "Need someone to talk to", "category": "Loneliness", "urgency": "medium", "location": "Downtown", "time_ago": "5 min ago", "urgency_color": "bg-orange-100 text-orange-800 border-orange-200"},
        {"id": "2", "title": "Help with anxiety management", "category": "Stress Handling", "urgency": "high", "location": "Westside", "time_ago": "12 min ago", "urgency_color": "bg-red-100 text-red-800 border-red-200"},
        {"id": "3", "title": "Practice conversation skills", "category": "Communication", "urgency": "low", "location": "East District", "time_ago": "1 hour ago", "urgency_color": "bg-blue-100 text-blue-800 border-blue-200"},
    ]

    your_chats = [
        {"id": "c1", "name": "Sarah M.", "message": "Thank you so much for your help!", "time": "2m ago", "unread": True},
        {"id": "c2", "name": "Mike T.", "message": "When would be a good time?", "time": "1h ago", "unread": False},
        {"id": "c3", "name": "Emma L.", "message": "I really appreciate you listening", "time": "3h ago", "unread": False},
    ]

    context = {
        "quick_stats": quick_stats,
        "recent_requests": recent_requests,
        "your_chats": your_chats,
    }
    return render(request, "HomePage.html", context)


def Signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, "signup.html")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, "signup.html")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        login(request, user)

        messages.success(request, "Account created successfully!")
        return redirect("/")

    return render(request, "signup.html")

def Login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # or wherever you want after login
        else:
            error = "Invalid email or password."
            return render(request, "login.html", {"error": error})

    return render(request, "login.html")

def Profile(request):
    stats = [
        ("Requests Fulfilled", 47, "text-rose-500", "❤️"),
        ("People Helped", 35, "text-blue-500", "👥"),
        ("This Month", 12, "text-green-500", "📈"),
        ("Impact Score", 850, "text-purple-500", "🏆"),
    ]

    category_progress = [
        {"category": "Weight Lifting", "count": 12, "icon": "💪", "color": "from-blue-500 to-cyan-500", "progress": 80},
        {"category": "Ride Sharing", "count": 8, "icon": "🚗", "color": "from-purple-500 to-pink-500", "progress": 55},
        {"category": "Electrical", "count": 15, "icon": "⚡", "color": "from-yellow-500 to-orange-500", "progress": 100},
        {"category": "Cleaning", "count": 7, "icon": "🧹", "color": "from-green-500 to-emerald-500", "progress": 45},
        {"category": "Pet Care", "count": 3, "icon": "🐕", "color": "from-rose-500 to-red-500", "progress": 20},
        {"category": "Moving", "count": 2, "icon": "📦", "color": "from-indigo-500 to-purple-500", "progress": 15},
    ]

    recent_activity = [
        {"action": "Helped with moving furniture", "person": "Sarah M.", "time": "2 hours ago", "category": "Moving"},
        {"action": "Fixed electrical outlet", "person": "Mike T.", "time": "1 day ago", "category": "Electrical"},
        {"action": "Gave ride to grocery store", "person": "Emma L.", "time": "2 days ago", "category": "Ride Sharing"},
        {"action": "Helped with garden cleanup", "person": "John D.", "time": "3 days ago", "category": "Cleaning"},
    ]

    achievements = [
        {"name": "First Helper", "description": "Completed your first request", "icon": "🎉", "unlocked": True},
        {"name": "Community Star", "description": "Helped 10 different people", "icon": "⭐", "unlocked": True},
        {"name": "Consistent Helper", "description": "Helped someone 7 days in a row", "icon": "🔥", "unlocked": True},
        {"name": "Neighborhood Hero", "description": "Completed 50 requests", "icon": "🦸", "unlocked": False},
        {"name": "Jack of All Trades", "description": "Helped in all categories", "icon": "🎯", "unlocked": False},
        {"name": "Early Bird", "description": "Accepted 5 requests within an hour", "icon": "🐦", "unlocked": True},
    ]

    return render(request, "profile.html", {
        "stats": stats,
        "category_progress": category_progress,
        "recent_activity": recent_activity,
        "achievements": achievements,
    })

def Requests(request):
    categories = [
        'All', 'Loneliness', 'Stress Handling', 'Communication', 'Weight Lifting',
        'Ride Sharing', 'Electrical', 'Cleaning', 'Pet Care', 'Tutoring', 'Shopping', 'Moving'
    ]

    selected_category = request.GET.get('category')

    # Filter the queryset
    if selected_category and selected_category != 'All':
        requests_qs = Request.objects.filter(category=selected_category)
    else:
        requests_qs = Request.objects.all()

    # Format for template
    requests_list = [
        {
            'id': r.id,
            'title': r.title,
            'description': r.description,
            'category': r.category,
            'location': r.location,
            'timeAgo': r.timeAgo,
            'urgency': r.urgency,
            'requester': {
                'name': r.requester_name,
                'initials': r.requester_initials,
            },
        }
        for r in requests_qs.order_by('-created_at')
    ]

    context = {
        'requests': requests_list,
        'categories': categories,
        'selected_category': selected_category,
    }

    return render(request, 'requests.html', context)



def add_request(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        category = request.POST.get("category")
        urgency = request.POST.get("urgency")
        location = request.POST.get("location")  # ✅ Add this line
        requester_name = "Anonymous"
        requester_initials = requester_name[:2].upper()

        Request.objects.create(
            title=title,
            description=description,
            category=category,
            urgency=urgency,
            location=location,
            requester_name=requester_name,
            requester_initials=requester_initials,
        )
        return redirect("requests")

def settings_page(request):
    return render(request, 'settings.html')
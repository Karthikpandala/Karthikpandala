export const mockData = {
  hero: {
    name: "Karthik Pandala",
    tagline: "Building Intelligent, Gesture-Driven Software",
    profileImage: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400' viewBox='0 0 400 400'%3E%3Ccircle cx='200' cy='200' r='200' fill='%23f4ce14'/%3E%3Cg transform='translate(80,120)'%3E%3Cpath d='M120 20 C140 10, 160 10, 180 20 C200 30, 210 60, 200 90 C190 120, 170 140, 150 140 C130 140, 110 120, 100 90 C90 60, 100 30, 120 20 Z' fill='%23d4af37'/%3E%3Cellipse cx='130' cy='80' rx='8' ry='12' fill='%23333'/%3E%3Cellipse cx='170' cy='80' rx='8' ry='12' fill='%23333'/%3E%3Cpath d='M140 100 Q150 110 160 100' stroke='%23333' stroke-width='3' fill='none'/%3E%3C/g%3E%3C/svg%3E"
  },
  about: {
    bio: "I'm a passionate Computer Science student and full-stack developer with expertise in building innovative applications that blend cutting-edge technology with user-centric design. My journey spans from gesture-controlled productivity tools to intelligent recommendation systems, always focused on creating meaningful digital experiences."
  },
  skills: {
    categories: [
      {
        name: "Programming Languages",
        items: ["C/C++", "Java", "JavaScript", "Python"]
      },
      {
        name: "Technologies & Frameworks",
        items: ["Node.js", "Electron.js", "REST APIs", "Streamlit"]
      },
      {
        name: "Databases & Tools",
        items: ["MySQL", "MongoDB", "Git", "Version Control"]
      },
      {
        name: "Concepts & Methodologies",
        items: ["SDLC", "Machine Learning", "Computer Vision", "Data Analysis"]
      },
      {
        name: "Soft Skills",
        items: ["Team Collaboration", "Problem Solving", "Time Management", "Communication"]
      }
    ]
  },
  projects: [
    {
      title: "Time Quacker: Gesture-Controlled Productivity Assistant",
      description: "An innovative desktop productivity application that revolutionizes time management through face detection and hand gesture recognition. Built with Electron.js, it combines Pomodoro timer functionality with cutting-edge computer vision technology.",
      image: "https://images.unsplash.com/photo-1628233345409-349459e6f79a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2MzR8MHwxfHNlYXJjaHwxfHxwcm9kdWN0aXZpdHklMjBhcHB8ZW58MHx8fHwxNzU0MDMwOTU3fDA&ixlib=rb-4.1.0&q=85",
      techStack: ["JavaScript", "Electron.js", "HTML", "Computer Vision", "Web APIs"],
      features: [
        "Face detection and hand gesture recognition for timer control",
        "Integrated hydration reminders with geolocation-based weather updates",
        "Modular architecture with camera selection and system tray integration",
        "Cross-platform compatibility with smooth, responsive UI",
        "Real-time speech API integration for voice feedback"
      ],
      githubLink: true,
      liveDemo: false
    },
    {
      title: "Movie Recommendation System",
      description: "An intelligent recommendation engine that suggests movies using advanced cosine similarity algorithms. Features an interactive frontend built with Streamlit and optimized machine learning models for precise recommendations.",
      image: "https://images.unsplash.com/photo-1685440663653-fa3e81dd109c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzB8MHwxfHNlYXJjaHwzfHxzdHJlYW1pbmclMjBhcHB8ZW58MHx8fHwxNzU0MDMwOTc4fDA&ixlib=rb-4.1.0&q=85",
      techStack: ["Python", "Machine Learning", "Streamlit", "Data Science", "Algorithms"],
      features: [
        "Cosine similarity algorithm for accurate movie matching",
        "Interactive web interface built with Streamlit framework",
        "Functional programming techniques for efficient model training",
        "Advanced data preprocessing and analytical optimization",
        "Collaborative filtering for enhanced recommendation precision"
      ],
      githubLink: true,
      liveDemo: true
    },
    {
      title: "Real-Time Weather Monitoring System",
      description: "A comprehensive weather monitoring application that provides real-time weather updates using the OpenWeatherMap API. Features a responsive design with automated validation and cloud-based data processing.",
      image: "https://images.unsplash.com/photo-1530563885674-66db50a1af19?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1NzZ8MHwxfHNlYXJjaHwyfHx3ZWF0aGVyJTIwYXBwfGVufDB8fHx8MTc1NDAzMDk3MXww&ixlib=rb-4.1.0&q=85",
      techStack: ["JavaScript", "Node.js", "Handlebars", "REST API", "CSS"],
      features: [
        "Real-time weather data integration with OpenWeatherMap API",
        "Responsive frontend design using Handlebars templating",
        "Automated API validation and error handling",
        "Cloud computing integration for improved data accuracy",
        "Comprehensive unit and integration testing suite"
      ],
      githubLink: true,
      liveDemo: true
    }
  ],
  certificates: [
    {
      title: "AI and Data Science Hackathon Winner",
      issuer: "Brainovision",
      year: "2023",
      description: "Won first place developing Optimized Manufacturing Planning (OMP) solutions for Aerospace Industry using Python, NumPy, Pandas, and Matplotlib."
    },
    {
      title: "5 Days Workshop on AI-ML and Data Science",
      issuer: "Tech Institute",
      year: "2023",
      description: "Intensive hands-on workshop covering data analytics, Python libraries, and machine learning concepts with practical project implementations."
    },
    {
      title: "Advanced Software Development Training",
      issuer: "Campus to Technical Careers",
      year: "2023",
      description: "Comprehensive training in Core Java 8, Hibernate, Spring Boot, full-stack development, and professional software development practices."
    }
  ],
  education: [
    {
      degree: "Bachelor of Technology, Computer Science Engineering",
      institution: "Sri Indu College of Engineering and Technology",
      period: "2021 – 2025",
      grade: "CGPA: 7.20",
      location: "Hyderabad, Telangana"
    },
    {
      degree: "Board of Intermediate Education",
      institution: "Narayana Junior College",
      period: "2019 – 2021",
      grade: "Percentage: 74.2%",
      location: "Hyderabad, Telangana"
    },
    {
      degree: "Board of Secondary Education",
      institution: "Naagarjuna High School",
      period: "2019",
      grade: "CGPA: 8.2",
      location: "Hyderabad, Telangana"
    }
  ],
  contact: {
    email: "karthikpandala0502@gmail.com",
    phone: "+91 8688262873",
    github: "https://github.com/karthikpandala",
    linkedin: "https://linkedin.com/in/karthikpandala"
  }
};
import React from "react";
import { Button } from "./ui/button";
import { Card, CardContent } from "./ui/card";
import { Badge } from "./ui/badge";
import { Separator } from "./ui/separator";
import { Github, Linkedin, Mail, Phone, ExternalLink, Award, GraduationCap } from "lucide-react";
import { mockData } from "../data/mock";

const Portfolio = () => {
  return (
    <div className="min-h-screen bg-slate-50">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-md z-50 border-b border-slate-200">
        <div className="container mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <div className="text-xl font-semibold text-slate-900">
              Karthik Pandala
            </div>
            <div className="hidden md:flex space-x-8">
              <a href="#about" className="text-slate-600 hover:text-blue-600 transition-colors">
                About
              </a>
              <a href="#projects" className="text-slate-600 hover:text-blue-600 transition-colors">
                Projects
              </a>
              <a href="#skills" className="text-slate-600 hover:text-blue-600 transition-colors">
                Skills
              </a>
              <a href="#contact" className="text-slate-600 hover:text-blue-600 transition-colors">
                Contact
              </a>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-24 pb-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="flex flex-col md:flex-row items-center gap-12">
            <div className="flex-1 space-y-6">
              <h1 className="text-4xl md:text-6xl font-light text-slate-900 leading-tight">
                Building Systems
                <br />
                <span className="font-semibold text-blue-600">That See</span>
              </h1>
              <h2 className="text-xl font-semibold text-slate-800 mb-2">
                Karthik Pandala
              </h2>
              <p className="text-lg md:text-xl text-slate-600 font-light max-w-lg">
                {mockData.hero.tagline}
              </p>
              <div className="flex gap-4 pt-4">
                <Button className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-full">
                  View Projects
                </Button>
                <Button variant="outline" className="border-slate-300 text-slate-700 hover:bg-slate-100 px-8 py-3 rounded-full">
                  Get In Touch
                </Button>
              </div>
            </div>
            <div className="flex-shrink-0">
              <div className="w-80 h-80 rounded-full overflow-hidden bg-gradient-to-br from-blue-400 to-blue-600 p-2">
                <img
                  src={mockData.hero.profileImage}
                  alt="Karthik Pandala"
                  className="w-full h-full object-cover rounded-full"
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-20 px-6 bg-white">
        <div className="container mx-auto max-w-4xl">
          <h2 className="text-3xl md:text-4xl font-light text-slate-900 mb-12 text-center">
            About Me
          </h2>
          <div className="prose prose-lg prose-slate mx-auto text-center">
            <p className="text-xl text-slate-600 leading-relaxed">
              {mockData.about.bio}
            </p>
          </div>
        </div>
      </section>

      {/* Skills Section */}
      <section id="skills" className="py-20 px-6 bg-slate-50">
        <div className="container mx-auto max-w-6xl">
          <h2 className="text-3xl md:text-4xl font-light text-slate-900 mb-16 text-center">
            Technical Skills
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {mockData.skills.categories.map((category, index) => (
              <Card key={index} className="bg-white border-slate-200 hover:shadow-lg transition-shadow">
                <CardContent className="p-6">
                  <h3 className="text-lg font-semibold text-slate-900 mb-4">
                    {category.name}
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {category.items.map((skill, skillIndex) => (
                      <Badge
                        key={skillIndex}
                        variant="secondary"
                        className="bg-slate-100 text-slate-700 hover:bg-blue-100 hover:text-blue-800 transition-colors"
                      >
                        {skill}
                      </Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Projects Section */}
      <section id="projects" className="py-20 px-6 bg-white">
        <div className="container mx-auto max-w-6xl">
          <h2 className="text-3xl md:text-4xl font-light text-slate-900 mb-16 text-center">
            Featured Projects
          </h2>
          <div className="space-y-16">
            {mockData.projects.map((project, index) => (
              <div
                key={index}
                className={`flex flex-col ${
                  index % 2 === 0 ? "lg:flex-row" : "lg:flex-row-reverse"
                } gap-12 items-center`}
              >
                <div className="flex-1">
                  <div className="bg-slate-100 rounded-2xl p-8 h-80 flex items-center justify-center overflow-hidden">
                    <img
                      src={project.image}
                      alt={project.title}
                      className="max-w-full max-h-full object-contain rounded-lg"
                    />
                  </div>
                </div>
                <div className="flex-1 space-y-6">
                  <h3 className="text-2xl md:text-3xl font-semibold text-slate-900">
                    {project.title}
                  </h3>
                  <p className="text-lg text-slate-600 leading-relaxed">
                    {project.description}
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {project.techStack.map((tech, techIndex) => (
                      <Badge
                        key={techIndex}
                        className="bg-blue-100 text-blue-800 hover:bg-blue-200 transition-colors"
                      >
                        {tech}
                      </Badge>
                    ))}
                  </div>
                  <ul className="space-y-2">
                    {project.features.map((feature, featureIndex) => (
                      <li key={featureIndex} className="text-slate-600 flex items-start gap-2">
                        <span className="w-1.5 h-1.5 bg-blue-600 rounded-full mt-2 flex-shrink-0"></span>
                        {feature}
                      </li>
                    ))}
                  </ul>
                  <div className="flex gap-4 pt-4">
                    {project.githubLink && (
                      <Button
                        variant="outline"
                        className="border-slate-300 text-slate-700 hover:bg-slate-100"
                      >
                        <Github className="w-4 h-4 mr-2" />
                        View Code
                      </Button>
                    )}
                    {project.liveDemo && (
                      <Button className="bg-blue-600 hover:bg-blue-700 text-white">
                        <ExternalLink className="w-4 h-4 mr-2" />
                        Live Demo
                      </Button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Certificates Section */}
      <section className="py-20 px-6 bg-slate-50">
        <div className="container mx-auto max-w-6xl">
          <h2 className="text-3xl md:text-4xl font-light text-slate-900 mb-16 text-center">
            Certificates & Achievements
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {mockData.certificates.map((cert, index) => (
              <Card key={index} className="bg-white border-slate-200 hover:shadow-lg transition-shadow">
                <CardContent className="p-6">
                  <div className="flex items-start gap-4">
                    <div className="p-3 bg-blue-100 rounded-lg flex-shrink-0">
                      <Award className="w-6 h-6 text-blue-600" />
                    </div>
                    <div className="space-y-2">
                      <h3 className="font-semibold text-slate-900">{cert.title}</h3>
                      <p className="text-sm text-slate-600">{cert.issuer} • {cert.year}</p>
                      <p className="text-sm text-slate-700">{cert.description}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Education Section */}
      <section className="py-20 px-6 bg-white">
        <div className="container mx-auto max-w-4xl">
          <h2 className="text-3xl md:text-4xl font-light text-slate-900 mb-16 text-center">
            Education
          </h2>
          <div className="space-y-8">
            {mockData.education.map((edu, index) => (
              <Card key={index} className="bg-slate-50 border-slate-200">
                <CardContent className="p-6">
                  <div className="flex items-start gap-4">
                    <div className="p-3 bg-blue-100 rounded-lg flex-shrink-0">
                      <GraduationCap className="w-6 h-6 text-blue-600" />
                    </div>
                    <div className="flex-1">
                      <div className="flex flex-col md:flex-row md:justify-between md:items-start gap-2">
                        <div>
                          <h3 className="text-xl font-semibold text-slate-900">{edu.degree}</h3>
                          <p className="text-slate-600">{edu.institution}</p>
                        </div>
                        <div className="text-right">
                          <p className="text-slate-600">{edu.period}</p>
                          <p className="text-slate-800 font-medium">{edu.grade}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="py-20 px-6 bg-slate-900">
        <div className="container mx-auto max-w-4xl text-center">
          <h2 className="text-3xl md:text-4xl font-light text-white mb-8">
            Let's Connect
          </h2>
          <p className="text-xl text-slate-300 mb-12">
            Ready to collaborate or have a question? I'd love to hear from you.
          </p>

          <div className="grid md:grid-cols-2 gap-8 mb-12">
            <Card className="bg-slate-800 border-slate-700">
              <CardContent className="p-6 text-center">
                <Mail className="w-8 h-8 text-blue-400 mx-auto mb-4" />
                <h3 className="text-white font-semibold mb-2">Email</h3>
                <p className="text-slate-300">{mockData.contact.email}</p>
              </CardContent>
            </Card>
            <Card className="bg-slate-800 border-slate-700">
              <CardContent className="p-6 text-center">
                <Phone className="w-8 h-8 text-blue-400 mx-auto mb-4" />
                <h3 className="text-white font-semibold mb-2">Phone</h3>
                <p className="text-slate-300">{mockData.contact.phone}</p>
              </CardContent>
            </Card>
          </div>

          <div className="flex justify-center gap-6">
            <Button
              variant="outline"
              size="lg"
              className="border-slate-600 text-slate-300 hover:bg-slate-800 hover:text-white"
            >
              <Github className="w-5 h-5 mr-2" />
              GitHub
            </Button>
            <Button
              variant="outline"
              size="lg"
              className="border-slate-600 text-slate-300 hover:bg-slate-800 hover:text-white"
            >
              <Linkedin className="w-5 h-5 mr-2" />
              LinkedIn
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 px-6 bg-slate-950 border-t border-slate-800">
        <div className="container mx-auto max-w-6xl">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-slate-400 text-sm">
              © 2024 Karthik Pandala. All rights reserved.
            </p>
            <p className="text-slate-500 text-sm">
              "Let's build something amazing together"
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Portfolio;
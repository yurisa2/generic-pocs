import json
from jinja2 import Environment, FileSystemLoader


# Set up the Jinja2 environment
file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)


data = """{
  "name": "Developer CoolName",
  "seniority_level": "Junior",
  "role": "Software Engineer",
  "summary": "A Junior Software Engineer with experience in Backend Technologies (Core Java, Hibernate, Spring Boot, Spring Data JPA, Optaplanner framework, Microservices), Databases (MySQL, PostgreSQL, Flyway), and Operating Systems (Windows, Linux).  Proficient in using Git for version control and possesses skills in MS Office suite.  Experienced in developing web applications using Java, Spring Boot, and various frameworks, demonstrating skills in implementing authentication and authorization, microservices architectures, and utilizing Optaplanner for scheduling optimization.",
  "skills": [
    {
      "category": "Languages and Frameworks",
      "skills": "Core Java, Hibernate, Spring Boot, Spring Data JPA, Optaplanner framework, Microservices"
    },
    {
      "category": "DBMS",
      "skills": "MySQL, PostgreSQL, Flyway"
    },
    {
      "category": "OS & Platforms",
      "skills": "Windows, Linux"
    },
    {
      "category": "SCM, Build, CI/CD",
      "skills": "Git"
    },
    {
      "category": "Other",
      "skills": "MS Word, MS PowerPoint, MS Excel"
    }
  ],
  "education": [
    {
      "institution": "S.D Vidya School, Ambala Cantt",
      "years": "2010",
      "degree": "10th"
    },
    {
      "institution": "S.D Vidya School, Ambala Cantt",
      "years": "2013",
      "degree": "12th"
    },
    {
      "institution": "University Institute of Engineering & Technology, Kurukshetra University",
      "years": "2017",
      "degree": "B.Tech(ECE)"
    }
  ],
  "certifications": [],
  "employment_history": [
    {
      "company": "Radiansys Technologies",
      "position": "Software Engineer",
      "years": "Dec 2022 - present",
      "description": null,
      "technologies": null,
      "activities_responsabilities": []
    },
    {
      "company": "NewgenSoft Technologies",
      "position": "Software Engineer",
      "years": "July 2022 – Nov 2022",
      "description": null,
      "technologies": null,
      "activities_responsabilities": []
    },
    {
      "company": "Oodles Technologies",
      "position": "Software Engineer",
      "years": "Jan 2021 – June 2022",
      "description": null,
      "technologies": null,
      "activities_responsabilities": []
    },
    {
      "company": "Piford Technologies",
      "position": "Industrial Training",
      "years": "July 2019 – Nov 2019",
      "description": null,
      "technologies": null,
      "activities_responsabilities": []
    },
    {
      "company": "Trisect Institute",
      "position": "Industrial Training",
      "years": "Aug 2017 – Oct 2017",
      "description": null,
      "technologies": null,
      "activities_responsabilities": []
    }
  ]
} """

data = json.loads(data)

# Load the template
template = env.get_template("resume-template-3.0.html")

# Render the template with the JSON data
output = template.render(data)

# Save the rendered output to a file
with open('output.html', 'w') as output_file:
    output_file.write(output)

print("Template rendered successfully.")

import json
from jinja2 import Environment, FileSystemLoader


# Set up the Jinja2 environment
file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)


data = """{  "name": "Erick Santillan Suarez",  "seniority_level": "Junior",  "role": "Developer",  "summary": "A passionate systems developer committed to continuous development of knowledge and skills, seeking to consolidate in a company to apply and expand skills.  Goal is to contribute to organizational growth while continuing to learn and face new challenges for personal and professional development.",  "skills": [    {      "category": "Languages and Frameworks",      "skills": "NodeJs, Express, ORM Sequelize, SQL, NoSQL, Bash Script, Java, Python, Flask, React, Angular, TypeScript, HTML5, CSS3, Bootstrap, Tailwind, JavaScript"    },    {      "category": "OS & Platforms",      "skills": "Linux"    },    {      "category": "DBMS",      "skills": "SQL, NoSQL"    },    {      "category": "SCM, Build, CI/CD",      "skills": "Git, Docker, Nginx, PM2"    },    {      "category": "Other",      "skills": "Data bases modelling, Projects maintenances, Testing, Code documentation, Statistical analysis, Predictive modeling, Mathematical optimization, Computational thinking"    }  ],  "education": [    {      "institution": "Polytechnic National Institute",      "years": "2016-2021",      "degree": "Bachelor of Economics"    },    {      "institution": "Open and Distance University of Mexico",      "years": "2017 - Present",      "degree": "Bachelor of Mathematics (50%)"    },    {      "institution": "School of Code of the Gov. of Mexico City",      "years": "Mar - Jun (2022)",      "degree": "Programming with Python"    },    {      "institution": "Polytechnic National Institute",      "years": "Sep - Nov (2019)",      "degree": "INEGI Microdata Management"    }  ],  "certifications": [],  "employment_history": [    {      "company": "INFOTEC",      "position": "Developer",      "years": "2023 Nov. – 2024 Sep.",      "description": "Main activities: Backend development, Frontend development, Data bases modelling, Projects maintenances, Testing, Code documentation",      "technologies": "NodeJs, Express, ORM Sequelize, SQL, NoSQL, Bash Script, Java, Python, Flask, React, Angular, TypeScript, HTML5, CSS3, Bootstrap, Tailwind, JavaScript",      "activities_responsabilities": [        "Backend development",        "Frontend development",        "Data bases modelling",        "Projects maintenances",        "Testing",        "Code documentation"      ]    },    {      "company": "CFE-TEIT",      "position": "Developer",      "years": "2022 Nov. – 2023 Νον.",      "description": "Main activities: All tasks listed above",      "technologies": "NodeJs, Express, ORM Sequelize, SQL, NoSQL, Bash Script, Java, Python, Flask, React, Angular, TypeScript, HTML5, CSS3, Bootstrap, Tailwind, JavaScript",      "activities_responsabilities": [        "Backend development",        "Frontend development",        "Data bases modelling",        "Projects maintenances",        "Testing",        "Code documentation"      ]    }  ]} """

data = json.loads(data)

# Load the template
template = env.get_template("resume-template-3.0.html")

# Render the template with the JSON data
output = template.render(data)

# Save the rendered output to a file
with open('output.html', 'w') as output_file:
    output_file.write(output)

print("Template rendered successfully.")

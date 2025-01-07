import functions_framework
from flask import request, jsonify
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import os
from dotenv import load_dotenv
import io
from jinja2 import Template

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")
vertexai.init(project=PROJECT_ID, location=REGION)

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "seniority_level": {"type": "string"},
        "role": {"type": "string"},
        "summary": {"type": "string"},
        "skills": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {"type": "string"},
                    "skills": {"type": "string"},
                },
                "required": ["category", "skills"],
            },
        },
        "education": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "institution": {"type": "string"},
                    "years": {"type": "string"},
                    "degree": {"type": "string"},
                },
                "required": ["institution", "years", "degree"],
            },
        },
        "certifications": {
            "type": "array",
            "items": {
                "type": "object"
                # You can further define properties for certifications if needed
            },
        },
        "employment_history": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "company": {"type": "string"},
                    "position": {"type": "string"},
                    "years": {"type": "string"},
                    "description": {"type": "string"},
                    "technologies": {"type": "string"},
                    "activities_responsabilities": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                "required": [
                    "company",
                    "position",
                    "years",
                    "activities_responsabilities",
                ],
            },
        },
    },
    "required": [
        "name",
        "seniority_level",
        "role",
        "summary",
        "skills",
        "education",
        "employment_history",
    ],
}


def extract_keys(schema, prefix=""):
    keys = []
    if schema.get("type") == "object":
        for key, value in schema.get("properties", {}).items():
            full_key = f"{prefix}.{key}" if prefix else key
            keys.append(full_key)
            keys.extend(extract_keys(value, prefix=full_key))
    elif schema.get("type") == "array":
        items = schema.get("items", {})
        keys.extend(extract_keys(items, prefix=f"{prefix}[]"))
    return keys


all_keys = extract_keys(schema)

@functions_framework.http
def get_file_and_add_prompt(request):
    if request.method != "POST":
        return jsonify({"error": "Only POST method is allowed"}), 405

    if "file_receive" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file_receive"]
    filename = file.filename
    file_extension = filename.split(".")[-1].lower()

    if file_extension == "pdf":
        try:
            # Read the PDF file content into memory
            pdf_content = file.read()

            # Create a Part object for the PDF data
            pdf_part = Part.from_data(
                pdf_content, mime_type="application/pdf"
            )

            generative_multimodal_model = GenerativeModel(
                "gemini-1.5-flash-002"
            )  # Use gemini-pro for multimodal
            prompt = """
                This is a CV file I need to extract the following information from the CV:
                
                Name
                Seniority Level, Junior, middle or Senior
                Role example as: Software Engineer, Full Stack Developer, Frontend Developer, Backend Developer, DevOps Engineer, Data Scientist, Data Analyst, Data Engineer, Machine Learning Engineer, AI Engineer, Cloud Engineer, Cloud Architect, Site Reliability Engineer (SRE), QA Engineer, QA Automation Engineer, QA Tester, QA Analyst, QA Lead, QA Manager, QA Director, QA VP
                
                Create a summary of the candidates professional life, here is an example:
                A highly skilled Lead Software Engineer with a focus on React, Angular, NodeJS, and Java offering a combination of cross-functional skills with 7+ years of commercial experience in Web Development and technical leadership experience. My expertise includes requirements gathering and analysis, business processes analysis and design, solution integration architecture, project architecture design, and deployment process setup.

                Skills, use only the labels "Languages and Frameworks", "OS & Platforms", "DBMS", "SCM, Build, CI/CD" and "Other",   example:
                Languages and Frameworks: JavaScript/EcmaScript 5/6/7, TypeScript, C#, SQL, Java, Flash/Flex, NodeJS, React/Redux, AngularJS, Common/Require, FabricJS, jQuery/jQueryUI, NightmareJS, PhantomJS, Electron, Twitter Bootstrap, OpentypeJS, JSE/JEE;

                OS & Platforms: MacOS, Linux, Windows; AWS;
                DBMS: MSSQL, Sequelize, Oracle/Hibernate;
                SCM, Build, CI/CD: Bitbucket/Github, Git, SVN; Npm/Bower, Babel, Webpack/Browserify, Grunt/Gulp, Ant, Maven; Codeship, TeamCity, Vagrant, Jenkins, Jira, Confluence;
                Other: OOP, SOLID, REST, Design Patterns, UI/UX Design, SOA, SPA; HTML5/CSS3, Flash/Flex, SCSS/LESS, Asp.Net Web Forms/Mvc; Ajax/Promises, Prototype/Closures, CORS, JSON/JSONP, RegExp.

                Education, example:
                National Technical University of Ukraine	2006 - 2012
                Degree, Major (can go on the 2nd line)
                Really long name of some university with very long name	2006 - 2012
                Degree, Major (can go on the 2nd line)

                Certifications, example:
                
                Microsoft MCPD Windows 4 	2012
                (Transcript: 952394; Access Code: 111111111)
                SCRUM Alliance ­Certified SCRUM Master	2010
                (Transcript: 952394; Access Code: 111111111)

                EMPLOYMENT HISTORY, for each employment history, get the company, position or role, years of work, general description of the job, technologies used and the activities and responabilities example:
                AgileEngine, Lead Fullstack Developer	2017 - Present
                Mi9 Retail is the premier provider of enterprise software including merchandising, business intelligence, and store operations for large and medium retailers. Mi9 Merchant is a state-of-the-art merchandise management system that provides meaningful visibility into shopper behavior, product performance, and vendor reliability. Designed for complex inventory and high SKU volume to address your extensive transaction processing needs, this solution delivers one source of information to support buying, pricing, inventory management, and inventory valuation.
                Activities and responsibilities:
                Leading and mentoring a team of 6 engineers
                Worked with the customer to collect, clarify, and capture requirements
                Responsible for architecture design, technical design, and task decomposition
                Responsible for core components implementation and architecture
                Communication with the onsite team & customers
                Project estimation & creation of project documentation
                Code refactoring and performance optimization
                Creating NPM/BASH scripts for the CI server
                Implementing SCRUM process
                Interviewing candidates

                Technologies:  JavaScript, TypeScript, AngularJS 1, ReactJS, Redux, RXJS, SCSS, CSS3, NodeJS, Babel, Webpack, Jest, NPM/Bash scripts, MSSQL.
                Company Name, Position Name	From Year - To Year
                Project Name - [position name for a] short description of the project for projects not similar to the target project. Provide a longer description for the projects that are relevant to the target customer.
                Activities and responsibilities:
                Keep the list of responsibilities to at most 4 line items for old projects
                Mention something really cool or relevant to the target position
                Avoid boilerplate responsibilities unless they match what’s needed
                See the example projects below for projects without technologies or list of responsibilities
                Technologies:  JavaScript, TypeScript, AngularJS 1, ReactJS, Redux, RXJS, SCSS, CSS3, NodeJS, Babel, Webpack, Jest, NPM/Bash scripts, MSSQL.

                Victor - Fly Smarter. Development of mobile application for charter requests.
                Activities and responsibilities:
                Integration with Rest API of node.js/.NET servers
                Salesforce, Mixpanel, GA integrations (including universal Segment.IO)
                Mobile security and PCI integrations with Stripe, Skrill, and Paysafe
                Full cycle development (Architecture design, technical design, tasks decomposition, estimating, development, dev testing)
                Location Services, APNS, CoreData, Multithreading, Background modes

                Foodora - building a mobile app for the food delivery service. Senior iOS Developer leading full cycle development, including architecture design, technical design, tasks decomposition, estimating, development, and testing.

                Internal Educational System - Lead Engineer for a system that allows users to check their lab works. The main idea is to run unit tests against the uploaded source files and return useful information about the results. The main requirement was to run test scenarios asynchronously. For this purpose, we use RabbitMQ as a communication protocol. The system is designed in microservices architecture with the aim of Spring Boot framework. The frontend part is built on Grails. Gradle is used for building sources and running tests.
                Technologies:  JavaScript, TypeScript, AngularJS 1, ReactJS, Redux, RXJS, SCSS, CSS3, NodeJS, Babel, Webpack, Jest, NPM/Bash scripts, MSSQL.

                
                get the response in JSON format as it follows on the spec below, but remove all definitions:

                {
  "type": "object",
  "properties": {
    "name": {
      "type": "string"
    },
    "seniority_level": {
      "type": "string"
    },
    "role": {
      "type": "string"
    },
    "summary": {
      "type": "string"
    },
    "skills": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "category": {
            "type": "string"
          },
          "skills": {
            "type": "string"
          }
        },
        "required": ["category", "skills"]
      }
    },
    "education": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "institution": {
            "type": "string"
          },
          "years": {
            "type": "string"
          },
          "degree": {
            "type": "string"
          }
        },
        "required": ["institution", "years", "degree"]
      }
    },
    "certifications": {
      "type": "array",
      "items": {
        "type": "object"
      }
    },
    "employment_history": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "company": {
            "type": "string"
          },
          "position": {
            "type": "string"
          },
          "years": {
            "type": "string"
          },
          "description": {
            "type": "string"
          },
          "technologies": {
            "type": "string"
          },
          "activities_responsabilities": {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        },
        "required": ["company", "position", "years", "activities_responsabilities"]
      }
    }
  },
  "required": ["name", "seniority_level", "role", "summary", "skills", "education", "employment_history"]
}
                
                """  # More specific prompt

            responses = generative_multimodal_model.generate_content(
                [prompt, pdf_part],
                generation_config={
                    "max_output_tokens": 8192  # Increase max output tokens for potentially long PDFs
                },
            )

            print(responses)

            text = responses.candidates[0].content.text  # Extract the text from the response

            text = text.replace("```json", "").replace("```", "").replace("\n", "").replace("\r", "").replace("\t", "")

            return jsonify(text), 200

        except Exception as e:
            print(f"Error processing PDF: {e}")  # Print the error for debugging
            return (
                jsonify({"error": f"Error processing PDF: {e}"}),
                500,
            )  # Return error to client

    else:
        return jsonify({"error": "Unsupported file type"}), 400

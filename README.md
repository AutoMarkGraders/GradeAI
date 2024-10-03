# GradeAI

**GradeAI** is a web-based AI Answer Paper Evaluator designed to revolutionize the education sector by automating the exam evaluation process. This system allows institutions to submit exam papers, get them evaluated, and view statistics and feedback through a user-friendly interface. The platform offers a personalized experience for both educators and students, reducing the workload on teachers and providing consistent and objective assessments of student performance.

## Features

- **Automated Exam Evaluation**: Evaluate handwritten answer sheets based on relevance, coherence, quality, and semantic similarity to the answer key.
- **Fast Processing**: At least 10x faster than traditional human evaluation processes.
- **Secure and Scalable**: Papers are securely processed and stored on the server, ensuring data integrity and confidentiality.
- **User Authentication**: Firebase authentication with email verification for secure access.
- **Personalized Dashboards**: Educators and students can view exam history, results, grades, and rankings through their respective dashboards.
- **Result Sharing**: Examination cells can share results with students, teachers, and the public as required.
- **Backend Deployment**: Deployed on an Azure Virtual Machine using Nginx with HTTPS enabled via Certbot SSL certification.

## SaaS Deployment

GradeAI is deployed as a Software-as-a-Service (SaaS) solution, meaning there is no need for users to install or set up anything locally. Institutions can simply sign up and start using the platform immediately.

## How It Works

1. **Sign Up**: Institutions create an account on the GradeAI platform.
2. **Submit Exams**: Upload handwritten answer sheets as PDF or image files, along with the corresponding answer key.
3. **Evaluation**: The system processes the submissions, evaluates the answer sheets, and assigns scores automatically.
4. **View Results**: Results, including grades and rankings, are available for viewing by educators, students, and other authorized users.

## Acknowledgements

- FastAPI: For creating an amazing framework for building APIs.
- Firebase: For providing robust authentication services.
- Azure: For reliable cloud hosting.
- Certbot: For easy SSL certificate management.

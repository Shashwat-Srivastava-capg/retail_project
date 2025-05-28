# 🤖 Google ADK + Chainlit: Build an AI Geolocation Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Made with Google ADK](https://img.shields.io/badge/Made%20with-Google%20ADK-blue)](https://cloud.google.com/adk)
[![Built with Chainlit](https://img.shields.io/badge/Built%20with-Chainlit-pink)](https://chainlit.io)

Learn how to build an intelligent AI agent using Google's AI Development Kit (ADK) - a powerful framework for developing AI agents - combined with Chainlit's modern chat interface. This tutorial demonstrates agent development by creating a geolocation assistant that converts coordinates into location names. Perfect for developers getting started with AI agent development! 🚀

### 🌟 Why This Project?
- Master Google ADK for AI agent development
- Learn agent-first development practices
- Create beautiful chat interfaces with Chainlit
- Implement real-world geolocation features
- Perfect starting point for building your own AI agents

## Educational Purpose 📚

This project is created as an open educational resource to help developers understand:
- How to integrate Google ADK with Chainlit
- Building interactive AI agents with modern tools
- Implementing geolocation features in chatbots
- Best practices for AI agent development

Feel free to use this code as a learning resource, modify it for your needs, or contribute improvements!

## Features ✨

- Built with Google ADK's agent development framework
- Interactive chat interface powered by Chainlit
- Intelligent coordinate-to-location conversion
- Integration with OpenCage Geocoding API
- Support for both light and dark themes
- Well-documented code for learning agent development

## Prerequisites 📋

Before running this application, make sure you have:

1. Python 3.9 or higher installed
2. An OpenCage API key (get one at [OpenCage](https://opencagedata.com/))
3. Google ADK access and credentials

## Installation 🚀

1. Clone the repository:
```bash
git clone git@github.com:Ngoga-Musagi/building-ai-agents-with-adk.git
cd building-ai-agents-with-adk
```

2. Create and activate a virtual environment (recommended):
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/MacOS
python -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your API keys:


## Usage 💡

1. Start the application:
```bash
chainlit run main.py
```

2. Open your browser and navigate to `http://localhost:8000`

3. Enter coordinates in the chat using formats like:
   - "What's at latitude 40.7128, longitude -74.0060?"
   - "Find the location at lat 48.8584, long 2.2945"

## Project Structure 📁

```
geolocation_agent/
├── main.py              # Main Chainlit application
├── agent.py            # Google ADK agent implementation
├── requirements.txt    # Project dependencies
├── .env               # Environment variables (not in repo)
├── chainlit.md        # Chainlit welcome screen
└── chainlit.config.toml # Chainlit configuration
```

## API Integration 🔌

The application leverages two main components:

1. **Google ADK**: A framework specifically designed for developing AI agents, providing:
   - Agent-centric development approach
   - Built-in tools and function handling
   - Seamless integration with Google's AI models
   - Structured agent behavior definition

2. **OpenCage Geocoding**: For converting coordinates to location names

## Contributing 🤝

This is an open educational project, and contributions are highly encouraged! Whether you're fixing bugs, improving documentation, or adding new features, your help is welcome.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2024 Ngoga Alexis

This project is open-source and free to use. You are welcome to use, modify, and distribute the code for any purpose, including educational and commercial use. The MIT License is chosen specifically to encourage sharing and learning.

## Acknowledgments 🙏

- [Google ADK](https://cloud.google.com/adk) for the AI capabilities
- [Chainlit](https://chainlit.io) for the chat interface
- [OpenCage](https://opencagedata.com/) for the geocoding service


## Support & Questions 💬

If you have questions about:
- How to use this code for learning
- Implementation details
- Integration challenges
- Feature requests or suggestions

Please feel free to:
1. Open an issue in the GitHub repository
2. Start a discussion
3. Submit a pull request with improvements
4. Connect with me on [LinkedIn](https://www.linkedin.com/in/alexis-ngoga-24460022b/) for direct questions or discussions

## Contact & Connect 🤝

- **Author**: Ngoga Alexis
- **LinkedIn**: [Alexis Ngoga](https://www.linkedin.com/in/alexis-ngoga-24460022b/)
- Feel free to connect with me on LinkedIn for:
  - Questions about the implementation
  - Discussions about AI and technology
  - Potential collaborations
  - General networking

Let's learn and build together! 🚀

## Environment Setup 🔑

1. Create a `.env` file in the project root directory
2. Add the following required environment variables:

```env
# Google AI settings
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_google_api_key_here

# OpenCage API Key
OPENCAGE_API_KEY=your_opencage_api_key_here
```

### Getting the API Keys 🔐

1. **Google API Key**:
   - Get your API key from [Google AI Studio](https://aistudio.google.com/apikey)
   - Copy the key and paste it in your `.env` file as `GOOGLE_API_KEY`

2. **OpenCage API Key**:
   - Get your API key from [OpenCage Dashboard](https://opencagedata.com/dashboard#geocoding)
   - Copy the key and paste it in your `.env` file as `OPENCAGE_API_KEY`

Make sure to keep your API keys secure and never commit them to version control. 
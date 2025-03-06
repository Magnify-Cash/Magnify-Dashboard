# Magnify Cash Financial Model

A comprehensive financial modeling dashboard for Magnify Cash's decentralized microlending platform. This application provides interactive projections, scenario analysis, and detailed metrics for the platform's growth and economics.

## Overview

This dashboard models Magnify Cash's innovative approach to microlending:
- AI-powered credit scoring with 99% fraud reduction
- Decentralized capital from stakers earning 13.8% yield
- Biometric verification through World ID
- Targeting $506B TAM by 2030

## Quick Start (Local Development)

1. Clone this repository:
   ```bash
   git clone https://github.com/your-org/magnify-modeling.git
   cd magnify-modeling
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application locally:
   ```bash
   streamlit run app.py
   ```

## Deployment Options

### 1. Streamlit Cloud (Recommended)

The easiest way to deploy the application:

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Select app.py as the main file
5. Click "Deploy"

### 2. Docker Deployment

Build and run using Docker:

1. Build the image:
   ```bash
   docker build -t magnify-model .
   ```

2. Run the container:
   ```bash
   docker run -p 8501:8501 magnify-model
   ```

### 3. Manual Server Deployment

For deploying on your own server:

1. Clone the repository on your server
2. Install system dependencies:
   ```bash
   sudo apt-get update
   sudo apt-get install python3-pip python3-venv
   ```

3. Use the deployment script:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

4. The app will be available at your-server-ip:8501

## Environment Variables

Configure these environment variables for production:

```bash
PORT=8501                      # Port to run the application
STREAMLIT_SERVER_PORT=8501     # Streamlit specific port
STREAMLIT_SERVER_ADDRESS=0.0.0.0  # Listen on all interfaces
```

## Security Considerations

1. Always use HTTPS in production
2. Set up authentication if needed
3. Configure proper firewall rules
4. Keep dependencies updated

## Monitoring

The application logs to:
- Application logs: `logs/app.log`
- Access logs: `logs/access.log`

Monitor these using your preferred logging solution.

## Scaling

For high-traffic scenarios:

1. Use a load balancer
2. Deploy multiple instances
3. Configure caching
4. Use a CDN for static assets

## Troubleshooting

Common issues and solutions:

1. Port already in use:
   ```bash
   sudo lsof -i :8501
   kill -9 <PID>
   ```

2. Permission issues:
   ```bash
   sudo chown -R $USER:$USER .
   ```

3. Memory issues:
   - Increase swap space
   - Upgrade server resources

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is proprietary and confidential. All rights reserved.

## Support

For support or inquiries, please contact the Magnify Cash team. 
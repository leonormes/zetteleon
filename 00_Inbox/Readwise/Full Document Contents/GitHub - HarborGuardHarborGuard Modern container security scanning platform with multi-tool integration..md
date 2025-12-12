# GitHub - HarborGuard/HarborGuard: Modern container security scanning platform with multi-tool integration.

![rw-book-cover](https://opengraph.githubassets.com/4779947629db69c2b34800782041ae3d51b092cc6d65a63c0368cac5e8d21297/HarborGuard/HarborGuard)

## Metadata
- Author: [[https://github.com/HarborGuard/]]
- Full Title: GitHub - HarborGuard/HarborGuard: Modern container security scanning platform with multi-tool integration.
- Category: #articles
- Summary: Harbor Guard is a web platform that helps scan and secure Docker container images using multiple tools. It shows results in easy-to-understand charts and lets users track changes over time. The tool also offers a REST API and supports exporting reports for better security management.
- URL: https://github.com/HarborGuard/HarborGuard

## Full Document
### HarborGuard/HarborGuard

Open more actions menu

### Harbor Guard

[![Next.js](https://camo.githubusercontent.com/376b3aeb4de5fbc91a77fb4cced89a6c40c85f977c3206d33990b147ff83f197/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4e6578742e6a732d31352e342e362d626c61636b3f7374796c653d666c61742d737175617265266c6f676f3d6e6578742e6a73)](https://nextjs.org/)
[![React](https://camo.githubusercontent.com/97415021b00d1d2091e6a7eaafd1e86d170a15eebf9f1915d111e2ae237b14d3/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f52656163742d31392e312e302d626c75653f7374796c653d666c61742d737175617265266c6f676f3d7265616374)](https://reactjs.org/)
[![TypeScript](https://camo.githubusercontent.com/4e8c3816d93d5d264ce20ccf9eff4c6ebe6435725f55e279e81d4bf75d897295/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f547970655363726970742d352e782d626c75653f7374796c653d666c61742d737175617265266c6f676f3d74797065736372697074)](https://www.typescriptlang.org/)
[![Prisma](https://camo.githubusercontent.com/87229d16bfee57faeb5600c037c5eff848e25a33dae45755d4a6f18a7e498707/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f507269736d612d362e31342e302d3244333734383f7374796c653d666c61742d737175617265266c6f676f3d707269736d61)](https://www.prisma.io/)
[![Docker](https://camo.githubusercontent.com/3562c018a4aea9585fbc155c41fa7ae480d1357c5a1b529a152303ec99ec2df1/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f636b65722d656e61626c65642d3234393645443f7374796c653d666c61742d737175617265266c6f676f3d646f636b6572)](https://www.docker.com/)
[![License](https://camo.githubusercontent.com/4b002a7a17ae192c6e577d09f272d630ca0e15cddf93d447689137b0e56a3d20/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4c6963656e73652d4d49542d677265656e3f7374796c653d666c61742d737175617265)](https://github.com/HarborGuard/HarborGuard/blob/main/LICENSE)
A comprehensive container security scanning platform that provides an intuitive web interface for managing and visualizing security assessments of Docker images.

#### Installation

##### Docker (Recommended)

Run Harbor Guard using Docker with a single command:

```
docker run -p 3000:3000 ghcr.io/harborguard/harborguard:latest
```

To give Harbor Guard access to your local images:

```
docker run -p 3000:3000 -v /var/run/docker.sock:/var/run/docker.sock ghcr.io/harborguard/harborguard:latest
```

Access the application at `http://localhost:3000`

#### Screenshots

[![Harbor Guard Dashboard](https://github.com/HarborGuard/HarborGuard/raw/main/assets/home.png)](https://github.com/HarborGuard/HarborGuard/blob/main/assets/home.png)
*Harbor Guard Dashboard - Container security scanning made simple*

##### Development Setup

1. Clone the repository:

```
git clone https://github.com/HarborGuard/HarborGuard.git
cd HarborGuard
```

2. Install dependencies:

```
npm install
```

3. Set up the database:

```
npx prisma migrate dev
```

4. Start the development server:

```
npm run dev
```

#### Purpose

Harbor Guard is a modern web application designed to streamline container security management by providing a unified interface for multiple scanning tools and advanced visualization capabilities.

##### Multi-Tool Security Scanning

[![Harbor Guard Scans](https://github.com/HarborGuard/HarborGuard/raw/main/assets/scan.png)](https://github.com/HarborGuard/HarborGuard/blob/main/assets/scan.png)
*Harbor Guard Dashboard - Container security scanning made simple*

Harbor Guard integrates and orchestrates multiple industry-standard security scanning tools:

* **[Trivy](https://github.com/aquasecurity/trivy)** - Comprehensive vulnerability scanner for containers
* **[Grype](https://github.com/anchore/grype)** - Vulnerability scanner by Anchore
* **[Syft](https://github.com/anchore/syft)** - Software Bill of Materials (SBOM) generator
* **[Dockle](https://github.com/goodwithtech/dockle)** - Container image linter for security and best practices
* **[OSV Scanner](https://github.com/google/osv-scanner)** - Open Source Vulnerability database scanner
* **[Dive](https://github.com/wagoodman/dive)** - Docker image layer analysis and optimization tool

##### Quality of Life Improvements

Harbor Guard addresses common pain points in container security workflows:

* **Unified Dashboard** - Single interface for all scanning tools instead of managing multiple CLI outputs
* **Historical Tracking** - Persistent storage and comparison of scan results over time
* **Report Export** - Download individual tool reports or complete ZIP packages for compliance
* **Real-time Monitoring** - Live scan progress tracking with WebSocket integration
* **Smart Filtering** - Dynamic filtering and sorting of vulnerabilities by severity, package, or CVE
* **Interactive Charts** - Click-to-navigate scatter plots for vulnerability analysis

##### Optimized Visualization Strategy

[![Harbor Guard Library](https://github.com/HarborGuard/HarborGuard/raw/main/assets/libraries.png)](https://github.com/HarborGuard/HarborGuard/blob/main/assets/libraries.png)
*Harbor Guard Dashboard - Container security scanning made simple*

The platform employs several innovative approaches to vulnerability data visualization:

###### Library Vulnerability Scatterplot

* **Multi-dimensional mapping** - X-axis represents severity levels, Y-axis shows vulnerability counts
* **Interactive filtering** - Toggle visibility by severity level with real-time count updates
* **Clickable exploration** - Navigate directly to library-specific analysis from chart points
* **Color-coded severity** - Consistent color scheme across all interfaces (red/orange/yellow/blue)

###### Layer-by-Layer Analysis

* **Horizontal tab navigation** - Each Docker layer gets its own tab for focused analysis
* **Dynamic sizing** - Tab layout adapts to any number of layers without breaking
* **File system exploration** - Detailed view of files added/modified in each layer
* **Size optimization insights** - Visual indicators for layer sizes and optimization opportunities

###### Findings Management

* **Severity-based grouping** - Organize findings by Critical, High, Medium, Low severity
* **Progress tracking** - Visual indicators for scan completion and remediation status
* **Export flexibility** - Individual JSON reports or complete ZIP archives
* **API accessibility** - Public REST endpoints for programmatic access to scan data

#### Features

##### 🔍 Comprehensive Scanning

* Support for 6 major container security tools
* Automatic vulnerability detection and classification
* Software Bill of Materials (SBOM) generation
* Container best practices validation
* Layer-by-layer image analysis

##### 📊 Advanced Visualization

* Interactive vulnerability scatter plots
* Historical scan comparison charts
* Real-time progress monitoring
* Severity-based filtering and grouping
* Responsive design for all screen sizes

##### 🚀 Developer Experience

* Modern React 19 + Next.js 15 architecture
* TypeScript for type safety
* Prisma ORM for database management
* Tailwind CSS for styling
* shadcn/ui component library

##### 📈 Enterprise Ready

* RESTful API for programmatic access
* Bulk report export capabilities
* Persistent scan history
* Scalable database design
* Docker-first deployment

#### API Endpoints

Harbor Guard provides REST API endpoints for programmatic access:

##### Scan Reports

* `GET /api/image/[name]/scan/[scanId]/[reportType]` - Download individual tool reports
* `GET /api/image/[name]/scan/[scanId]/download` - Download complete scan package
* `GET /api/scans` - List all scans
* `POST /api/scans/start` - Initiate new scan

##### Docker Integration

* `GET /api/docker/images` - List local Docker images
* `GET /api/docker/search` - Search Docker Hub
* `GET /api/docker/info` - Docker daemon information

#### Architecture

Harbor Guard is built with modern web technologies:

* **Frontend**: React 19 + Next.js 15 with App Router
* **Styling**: Tailwind CSS + shadcn/ui components
* **Database**: SQLite with Prisma ORM
* **Charts**: Recharts for data visualization
* **Icons**: Tabler Icons + Lucide React
* **State Management**: React Context + Custom hooks

#### Contributing

We welcome contributions! Please see our [Contributing Guidelines](https://github.com/HarborGuard/HarborGuard/blob/main/CONTRIBUTING.md) for details.

##### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Run the test suite: `npm test`
6. Submit a pull request

#### License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/HarborGuard/HarborGuard/blob/main/LICENSE) file for details.

#### Support

* 🐛 [Report Issues](https://github.com/HarborGuard/HarborGuard/issues)
* 💬 [Discussions](https://github.com/HarborGuard/HarborGuard/discussions)
* 📧 [Email Support](mailto:support@harborguard.io)

#### Acknowledgments

Special thanks to the maintainers of the integrated security tools:

* Aqua Security (Trivy)
* Anchore (Grype, Syft)
* goodwithtech (Dockle)
* Google (OSV Scanner)
* wagoodman (Dive)

**Harbor Guard** - Securing containers, one scan at a time.

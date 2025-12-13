import re
from typing import List

class SkillExtractor:
    """Extract skills from resume text"""
    
    # Common technical skills keywords
    SKILL_KEYWORDS = [
        # Programming Languages
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust',
        'ruby', 'php', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql',
        'perl', 'lua', 'dart', 'haskell', 'erlang', 'elixir', 'clojure',
        'f#', 'ocaml', 'cobol', 'fortran', 'assembly', 'objective-c',
        
        # Web Frameworks & Libraries
        'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'fastapi',
        'spring', 'express', 'next.js', 'nuxt.js', 'svelte', 'ember',
        'laravel', 'symfony', 'rails', 'asp.net', 'jquery', 'bootstrap',
        'tailwind css', 'material-ui', 'ant design', 'chakra ui',
        
        # Mobile Development
        'react native', 'flutter', 'xamarin', 'ionic', 'cordova',
        'android studio', 'xcode', 'swiftui', 'jetpack compose',
        
        # ML/AI Frameworks & Libraries
        'tensorflow', 'pytorch', 'keras', 'pandas', 'numpy', 'scikit-learn',
        'scipy', 'matplotlib', 'seaborn', 'plotly', 'jupyter', 'opencv',
        'nltk', 'spacy', 'transformers', 'hugging face', 'langchain',
        'xgboost', 'lightgbm', 'catboost', 'pytorch lightning',
        
        # Cloud Platforms & Services
        'aws', 'azure', 'gcp', 'google cloud', 'oracle cloud', 'ibm cloud',
        'lambda', 'ec2', 's3', 'rds', 'dynamodb', 'cloudfront', 'route53',
        'azure functions', 'azure devops', 'app service', 'cosmos db',
        'firebase', 'vercel', 'netlify', 'heroku', 'digitalocean',
        
        # Containers & Orchestration
        'docker', 'kubernetes', 'docker compose', 'podman', 'containerd',
        'helm', 'istio', 'linkerd', 'rancher', 'openshift',
        
        # Databases
        'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch',
        'cassandra', 'couchdb', 'neo4j', 'dynamodb', 'couchbase',
        'oracle', 'sql server', 'sqlite', 'mariadb', 'influxdb',
        'timescaledb', 'cockroachdb', 'snowflake', 'bigquery',
        
        # DevOps & CI/CD Tools
        'git', 'github', 'gitlab', 'bitbucket', 'jenkins', 'circleci',
        'travis ci', 'github actions', 'gitlab ci', 'azure pipelines',
        'terraform', 'ansible', 'puppet', 'chef', 'vagrant',
        'prometheus', 'grafana', 'elk stack', 'splunk', 'datadog',
        'new relic', 'sentry', 'cloudwatch', 'azure monitor',
        
        # Operating Systems & Shells
        'linux', 'unix', 'bash', 'powershell', 'zsh', 'fish',
        'ubuntu', 'centos', 'debian', 'red hat', 'windows server',
        'macos', 'ios', 'android',
        
        # Data & Analytics
        'machine learning', 'deep learning', 'data science', 'data analysis',
        'big data', 'hadoop', 'spark', 'kafka', 'flink', 'storm',
        'tableau', 'power bi', 'qlik', 'looker', 'metabase',
        'apache airflow', 'luigi', 'prefect', 'dbt', 'databricks',
        'snowflake', 'redshift', 'hive', 'pig', 'hbase',
        
        # API & Web Services
        'rest api', 'graphql', 'grpc', 'soap', 'webhook',
        'oauth', 'jwt', 'openapi', 'swagger', 'postman',
        'api gateway', 'kong', 'nginx', 'apache', 'caddy',
        
        # Frontend Technologies
        'html', 'css', 'sass', 'less', 'stylus', 'webpack', 'vite',
        'npm', 'yarn', 'pnpm', 'babel', 'eslint', 'prettier',
        'typescript', 'webassembly', 'pwa', 'service workers',
        
        # Testing Frameworks
        'jest', 'mocha', 'chai', 'cypress', 'selenium', 'pytest',
        'junit', 'testng', 'rspec', 'phpunit', 'xunit',
        'playwright', 'puppeteer', 'karma', 'vitest',
        
        # Methodologies & Practices
        'agile', 'scrum', 'kanban', 'devops', 'ci/cd', 'tdd',
        'bdd', 'pair programming', 'code review', 'gitflow',
        'microservices', 'serverless', 'event-driven', 'domain-driven design',
        
        # Security
        'owasp', 'penetration testing', 'vulnerability assessment',
        'ssl/tls', 'encryption', 'oauth2', 'saml', 'ldap',
        'waf', 'ddos protection', 'security audit',
        
        # Version Control & Collaboration
        'git', 'svn', 'mercurial', 'perforce', 'confluence', 'jira',
        'slack', 'microsoft teams', 'trello', 'asana', 'notion',
        
        # Other Technologies
        'blockchain', 'ethereum', 'solidity', 'web3', 'smart contracts',
        'iot', 'arduino', 'raspberry pi', 'mqtt', 'coap',
        'vr', 'ar', 'unity', 'unreal engine', 'opengl', 'vulkan',
        'graphql', 'apollo', 'relay', 'prisma', 'hasura',
        'electron', 'tauri', 'nw.js', 'pwa', 'webgl',
        'websocket', 'socket.io', 'signalr', 'pusher',
        'rabbitmq', 'activemq', 'nats', 'pulsar',
        'elastic stack', 'logstash', 'kibana', 'beats',
        'prometheus', 'grafana', 'jaeger', 'zipkin',
    ]
    
    def extract_skills(self, resume_text: str) -> List[str]:
        """
        Extract skills from resume text using keyword matching
        """
        if not resume_text:
            return []
        
        text_lower = resume_text.lower()
        found_skills = []
        
        # Check for each skill keyword
        for skill in self.SKILL_KEYWORDS:
            # Use word boundaries for better matching
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill.title())
        
        # Remove duplicates and return
        return sorted(list(set(found_skills)))


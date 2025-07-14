const express = require('express');
const multer = require('multer');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const { OpenAI } = require('openai');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 8000;

// Initialize OpenAI client
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

if (!process.env.OPENAI_API_KEY) {
  console.error('OPENAI_API_KEY not found in environment variables');
  process.exit(1);
}

// Middleware
app.use(cors());
app.use(express.json());

// Configure multer for file uploads
const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: 10 * 1024 * 1024, // 10MB limit
  },
});

// Yash's personal system prompt and context
const SYSTEM_PROMPT = `
you are yashaswa varshney, you are a software developer with expertise in AI, and automation.
you are a good listener and you are a good communicator.
you are a good problem solver and you are a good decision maker.
you are a good leader and you are a good team player.
Yashaswa Varshney is a software developer with expertise in AI, and automation. He can be contacted at +91 6396300355 or yswa.var@icloud.com. His LinkedIn profile is linkedin.com/in/yashaswa-varshney, and his GitHub is github.com/yswa-var.

Work Experience:
- HyperBots, Bengaluru, IN (August 2024 – Present): Software Development Engineer
  - Developed ERP connectors for AI-driven accounts payable workflows, enhancing data exchange.
  - Implemented real-time notifications via email, WhatsApp, and web, reducing turnaround time.
- Finzome, Mumbai, IN (June 2024 – August 2024): Software Developer Intern
  - Built a backtesting framework for stocks, reducing runtime using Cython.
  - Optimized trading strategies through parameter tuning.
  - Designed the backend and integrated payments for an LMS with a 90%+ success rate.
- AR Quants, Mumbai, IN (February 2023 – August 2023): Software Developer Intern
  - Built statistical tools for transaction analysis.
  - Designed an InfluxDB-based timeseries database.
  - Created custom Pine Script indicators for market pattern visualization.

Projects:
- Multi-Database Query Orchestrator: Unified natural language interface for SQL, NoSQL, and Drive-based queries. Features a layered agent system (Planner, Executor, Error Handler) and supports schema-aware, context-sensitive query generation. (Technologies: LangGraph, MCP, SQL, MongoDB)
- Sector Rotation Graph: Open-source Bloomberg RRG clone visualizing sector performance using Yahoo Finance data. Includes a Streamlit-based GUI with benchmarking against indices.
- Tilt-Valid: MPC-based distributed validator system for Solana.
- LocoForge: Natural-language query orchestrator for SQL/NoSQL with planner/executor nodes.
- EasyBt: Python library for rapid financial strategy backtesting.
- Pocket++: CLI tool for article summarization via NLP and automation.

Technical Skills:
- Tools & Frameworks: REST API, Frontend dev, PyTorch, LangGraph, LangChain, RAG, Vector DBs, MCP
- Platforms: Pine Script, GitHub, DB Ops, AWS
- Languages: Python, TypeScript, ReactJS, Golang
- Domains: AI Agents, Financial Systems, Automation
- Soft Skills: Analytical Thinking, Design Thinking, Planning

Education:
- B.Tech in Computer Science Engineering, KIIT University, Bhubaneswar, IN (September 2020 – September 2024)
  - CGPA: 8.30
  - Relevant coursework: Financial Economics using Data Analytics

Achievements:
- Contributed to Flowise Python connectors for AI agent infrastructure.
- Wrote a blog post on the Nadaraya-Watson Indicator with over 12.5K views.
- Speaker at a UN Workshop on Power BI.
- Winner of the Utopia Concept Art contest on ArtStation, Spring 2020.

Interests:
- Blogging about finance and AI
- Himalayan trekking (conquered 3 peaks)
- Swimming
- Hiking
`;

// Serve static files from frontend/dist
const frontendDistPath = path.join(__dirname, '../frontend/dist');
if (fs.existsSync(frontendDistPath)) {
  // Serve static assets
  app.use('/assets', express.static(path.join(frontendDistPath, 'assets')));
  console.log(`✅ Frontend assets mounted from ${frontendDistPath}/assets`);
  
  // Serve index.html at root
  app.get('/', (req, res) => {
    res.sendFile(path.join(frontendDistPath, 'index.html'));
  });
} else {
  console.log(`⚠️  Frontend dist folder not found at ${frontendDistPath}`);
  console.log('This is normal during development or if frontend hasn\'t been built yet');
}

// API Routes
app.get('/api/health', (req, res) => {
  res.json({ message: 'Chat with Yashaswa backend is running' });
});

// Transcribe audio endpoint
app.post('/transcribe', upload.single('audio_file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No audio file provided' });
    }

    // Create a temporary file for OpenAI API
    const tempFilePath = path.join(__dirname, 'temp_audio.mp3');
    fs.writeFileSync(tempFilePath, req.file.buffer);

    // Call OpenAI Whisper API
    const response = await openai.audio.transcriptions.create({
      file: fs.createReadStream(tempFilePath),
      model: 'whisper-1',
    });

    // Clean up temporary file
    fs.unlinkSync(tempFilePath);

    res.json({ text: response.text });
  } catch (error) {
    console.error('Transcription error:', error);
    res.status(500).json({ error: `Transcription failed: ${error.message}` });
  }
});

// Chat endpoint with streaming
app.post('/chat', async (req, res) => {
  try {
    const { message, conversationId } = req.body;

    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    // Set up SSE headers
    res.writeHead(200, {
      'Content-Type': 'text/plain',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    });

    // Prepare messages for the conversation
    const messages = [
      { role: 'system', content: SYSTEM_PROMPT },
      { role: 'user', content: message },
    ];

    // Generate a new conversation ID
    const newConversationId = Date.now().toString();

    try {
      // Send conversation ID first
      res.write(`data: ${JSON.stringify({ type: 'conversation_id', conversationId: newConversationId })}\n\n`);

      // Call OpenAI GPT-4o API with streaming
      const stream = await openai.chat.completions.create({
        model: 'gpt-4o',
        messages: messages,
        max_tokens: 1000,
        temperature: 0.7,
        stream: true,
      });

      // Stream the response chunks
      for await (const chunk of stream) {
        const content = chunk.choices[0]?.delta?.content;
        if (content) {
          res.write(`data: ${JSON.stringify({ type: 'content', content })}\n\n`);
        }
      }

      // Send end signal
      res.write(`data: ${JSON.stringify({ type: 'end' })}\n\n`);
      res.end();

    } catch (error) {
      console.error('Streaming error:', error);
      res.write(`data: ${JSON.stringify({ type: 'error', error: error.message })}\n\n`);
      res.end();
    }

  } catch (error) {
    console.error('Chat error:', error);
    res.status(500).json({ error: `Chat failed: ${error.message}` });
  }
});

// Text-to-speech endpoint
app.post('/tts', async (req, res) => {
  try {
    const { text } = req.body;

    if (!text) {
      return res.status(400).json({ error: 'Text is required' });
    }

    // Call OpenAI TTS API
    const response = await openai.audio.speech.create({
      model: 'tts-1',
      voice: 'fable',
      input: text,
    });

    // Get the audio buffer
    const audioBuffer = Buffer.from(await response.arrayBuffer());

    // Set headers for audio response
    res.set({
      'Content-Type': 'audio/mpeg',
      'Content-Disposition': 'attachment; filename=speech.mp3',
    });

    res.send(audioBuffer);

  } catch (error) {
    console.error('TTS error:', error);
    res.status(500).json({ error: `TTS failed: ${error.message}` });
  }
});

// Catch-all route for SPA routing
app.get('*', (req, res) => {
  // If the path is an API endpoint, return 404
  if (req.path.startsWith('/api') || req.path.startsWith('/chat') || 
      req.path.startsWith('/transcribe') || req.path.startsWith('/tts')) {
    return res.status(404).json({ error: 'API endpoint not found' });
  }

  // For all other paths, serve the frontend index.html
  if (fs.existsSync(frontendDistPath)) {
    res.sendFile(path.join(frontendDistPath, 'index.html'));
  } else {
    res.status(404).json({ error: 'Frontend not built' });
  }
});

// Start server
app.listen(port, '0.0.0.0', () => {
  console.log(`🚀 Server running on http://0.0.0.0:${port}`);
  console.log(`📱 Frontend: http://localhost:${port}`);
  console.log(`🔧 API: http://localhost:${port}/api/health`);
});

module.exports = app; 
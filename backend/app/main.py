from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="DATASOPH AI",
    description="AI Data Scientist Backend",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "🚀 DATASOPH AI Backend is running!",
        "status": "success",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "DATASOPH AI",
        "version": "1.0.0",
        "endpoints": ["/", "/health", "/chat", "/docs"]
    }

@app.post("/chat")
async def chat(data: dict):
    message = data.get("message", "Hello")
    
    # Natural language responses based on message content
    message_lower = message.lower()
    
    if "hello" in message_lower or "hi" in message_lower:
        response = "Merhaba! Ben DATASOPH AI, veri bilimi konusunda size yardımcı olmaya hazırım. Hangi konuda çalışmak istiyorsunuz?"
    
    elif "data" in message_lower or "veri" in message_lower or "dataset" in message_lower:
        response = "Veri analizi konusunda size yardımcı olabilirim. Hangi tür veri üzerinde çalışıyorsunuz? CSV, Excel dosyası yükleyebilir veya mevcut verileriniz hakkında sorular sorabilirsiniz."
    
    elif "analysis" in message_lower or "analiz" in message_lower:
        response = "Veri analizi yapmak için dosyanızı yükleyebilirsiniz. Size istatistiksel analiz, korelasyon testleri ve görselleştirmeler sunabilirim. Hangi analizi yapmak istiyorsunuz?"
    
    elif "statistics" in message_lower or "istatistik" in message_lower:
        response = "İstatistiksel analiz konusunda uzmanım. T-test, ANOVA, korelasyon analizi, regresyon ve daha fazlasını yapabilirim. Hangi istatistiksel test hakkında bilgi almak istiyorsunuz?"
    
    elif "help" in message_lower or "yardım" in message_lower:
        response = "Size nasıl yardımcı olabilirim? Veri analizi, istatistiksel testler, görselleştirme, makine öğrenmesi önerileri veya iş zekası konularında destek verebilirim."
    
    elif "?" in message:
        response = "Bu konuda size yardımcı olabilirim. Daha detaylı bilgi vermek için dosyanızı yükleyebilir veya spesifik sorularınızı sorabilirsiniz."
    
    else:
        response = f"'{message}' hakkında konuşuyorsunuz. Bu konuda size nasıl yardımcı olabilirim? Veri analizi, istatistiksel testler veya görselleştirme konularında destek verebilirim."
    
    return {
        "response": response,
        "status": "success"
    }

@app.post("/analyze")
async def analyze(data: dict):
    return {
        "analysis": "Data analysis complete",
        "insights": ["This is a sample insight", "Data looks good"],
        "status": "success"
    }

# Run the app
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 
import type { GenAIRequest, GenAIResponse } from '../types/index.js';
export declare class GenAIService {
    private apiKey;
    constructor(apiKey?: string);
    analyzeCompliance(request: GenAIRequest): Promise<GenAIResponse>;
    extractText(buffer: Buffer, mimeType: string): Promise<string>;
}
export declare const genaiService: GenAIService;
//# sourceMappingURL=genai.d.ts.map
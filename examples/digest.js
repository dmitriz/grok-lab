#!/usr/bin/env node

/**
 * Simple News Digest Generator using Grok-3 API (JavaScript/Node.js version)
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

function loadKey(keyName, filePath) {
    try {
        const content = fs.readFileSync(filePath, 'utf8');
        const lines = content.split('\n');
        
        for (const line of lines) {
            const trimmed = line.trim();
            if (!trimmed || trimmed.startsWith('#')) {
                continue;
            }
            if (trimmed.includes('=')) {
                const [key, value] = trimmed.split('=', 2);
                if (key.trim() === keyName) {
                    return value.trim();
                }
            }
        }
        return null;
    } catch (error) {
        return null;
    }
}

function getApiKey() {
    const secretsPath = path.join(__dirname, '..', '.secrets', 'grok_keys.env');
    const apiKey = loadKey('GROK_API_KEY', secretsPath);
    
    if (!apiKey) {
        throw new Error(`Could not find GROK_API_KEY in ${secretsPath}`);
    }
    
    return apiKey;
}

function createRequestPayload() {
    return {
        messages: [
            {
                role: "user",
                content: "Provide me a digest of world news in the last 24 hours."
            }
        ],
        search_parameters: {
            mode: "auto"
        },
        model: "grok-3-latest"
    };
}

function callGrokApi(apiKey, payload) {
    return new Promise((resolve, reject) => {
        const data = JSON.stringify(payload);
        
        const options = {
            hostname: 'api.x.ai',
            port: 443,
            path: '/v1/chat/completions',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`,
                'Content-Length': Buffer.byteLength(data)
            },
            timeout: 60000
        };

        const req = https.request(options, (res) => {
            let responseData = '';

            res.on('data', (chunk) => {
                responseData += chunk;
            });

            res.on('end', () => {
                try {
                    const jsonResponse = JSON.parse(responseData);
                    resolve(jsonResponse);
                } catch (error) {
                    reject(new Error(`Failed to parse JSON response: ${error.message}`));
                }
            });
        });

        req.on('error', (error) => {
            reject(new Error(`API request failed: ${error.message}`));
        });

        req.on('timeout', () => {
            req.destroy();
            reject(new Error('API request timed out after 60 seconds'));
        });

        req.write(data);
        req.end();
    });
}

async function main() {
    try {
        console.log('Starting JavaScript news digest generation...');
        
        const apiKey = getApiKey();
        console.log('API key loaded successfully');
        
        const payload = createRequestPayload();
        console.log('Request payload created');
        
        console.log('Making API request...');
        const startTime = Date.now();
        const responseJson = await callGrokApi(apiKey, payload);
        const endTime = Date.now();
        
        console.log(`API call completed in ${endTime - startTime}ms`);
        console.log(JSON.stringify(responseJson, null, 2));
        
    } catch (error) {
        console.error(`Error: ${error.message}`);
        process.exit(1);
    }
}

if (require.main === module) {
    main();
}

module.exports = { loadKey, getApiKey, createRequestPayload, callGrokApi, main };

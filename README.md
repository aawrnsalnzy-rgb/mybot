# 🔓 Universal Lua Deobfuscator Discord Bot

A powerful Discord bot that deobfuscates multiple types of Lua obfuscators including Moonsec V3, IronBrew, Luarmor, WeAreDevs, and Veil.

## 🚀 Quick Setup

### Option 1: Import to Replit (Recommended)
1. **Import this repository** - Go to [Replit](https://replit.com) and click "Import from GitHub"
2. **Paste the repository URL** - Use the GitHub URL of this project
3. **Add Bot Credentials** - Go to the "Secrets" tab and add:
   - `DISCORD_TOKEN` = Your Discord bot token
   - `CLIENT_ID` = Your Discord application client ID
4. **Click Run** - The bot will start automatically!

### Option 2: Local Development
1. **Clone the repository**
   \`\`\`bash
   git clone https://github.com/yourusername/lua-deobfuscator-bot.git
   cd lua-deobfuscator-bot
   \`\`\`

2. **Install dependencies**
   \`\`\`bash
   npm install
   \`\`\`

3. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Add your Discord bot credentials:
     \`\`\`env
     DISCORD_TOKEN=your_bot_token_here
     CLIENT_ID=your_bot_client_id_here
     \`\`\`

4. **Start the bot**
   \`\`\`bash
   npm start
   \`\`\`

### Option 3: Deploy to Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)]([https://heroku.com/deploy](https://www.heroku.com/deploy/?template=https://github.com/heroku/nodejs-getting-started))

1. Click the deploy button above
2. Set the required environment variables in Heroku
3. Deploy and your bot will be online!

### Option 4: Deploy with Docker
\`\`\`bash
docker build -t lua-deobfuscator-bot .
docker run -e DISCORD_TOKEN=your_token -e CLIENT_ID=your_client_id lua-deobfuscator-bot
\`\`\`

## 🤖 Supported Obfuscators

- **Moonsec V3** - String tables, variable obfuscation
- **IronBrew** - Hex encoding, getfenv/setfenv patterns
- **Luarmor** - Uppercase variables, bit32 operations
- **WeAreDevs** - Base64 decoding
- **Veil** - Escape sequence decoding
- **Generic** - Fallback for unknown obfuscators

## 📋 Commands

### `/deobf code <input>`
Deobfuscate code directly by pasting it into the command.

### `/deobf url <link>`
Fetch and deobfuscate code from any URL (Pastebin, GitHub, etc.).

### `/deobf file <attachment>`
Upload a `.lua`, `.txt`, `.luau`, or `.luac` file to deobfuscate.

## ✨ Features

- 🔍 **Automatic Detection** - Identifies obfuscator type automatically
- 📊 **Detailed Statistics** - Shows variables renamed, strings replaced, etc.
- 📁 **File Output** - Always returns results as downloadable `.txt` files
- 🛡️ **Error Handling** - User-friendly error messages and validation
- 📱 **Multiple Input Methods** - Code, URLs, and file uploads
- 🎯 **Smart Processing** - Handles files up to 10MB and 500KB of code

## 🔧 Getting Your Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Copy the token and add it to Replit Secrets or your `.env` file as `DISCORD_TOKEN`
5. Copy the Application ID from "General Information" and add as `CLIENT_ID`
6. Invite the bot to your server with the "bot" and "applications.commands" scopes

## 🎮 Usage Example

\`\`\`
/deobf code local a = {"Hello", "World"}; print(a[1] .. " " .. a[2])
\`\`\`

The bot will automatically detect the obfuscation type, process the code, and return a clean, readable version as a downloadable file.

## 🔒 Permissions Required

- Send Messages
- Use Slash Commands  
- Attach Files
- Embed Links

## 🚀 Deployment Options

### Replit (Easiest)
- Import from GitHub to Replit
- Add tokens to Secrets tab
- Click Run - that's it!
- Perfect for beginners

### Heroku
- Use the deploy button above
- Set environment variables in Heroku dashboard
- Uses the included `Procfile`

### Railway
- Connect your GitHub repository
- Set environment variables
- Auto-deploys on push

### Docker
- Build with the included `Dockerfile`
- Run with environment variables
- Perfect for VPS deployment

### Local Development
- Clone and run with `npm start`
- Great for testing and development

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues:
1. Check the [Issues](https://github.com/yourusername/lua-deobfuscator-bot/issues) page
2. Create a new issue with detailed information
3. Include error logs and steps to reproduce

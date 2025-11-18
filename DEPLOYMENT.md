# Streamlit Cloud Deployment Guide

This guide walks you through deploying the Multi-Language Code Analyzer to Streamlit Cloud.

## Prerequisites

- GitHub account
- Streamlit Cloud account (free at https://share.streamlit.io/)
- Gemini API key (optional, for LLM features)

## Deployment Steps

### Step 1: Prepare Your Repository

1. **Build grammars locally** (recommended approach):
   ```bash
   python build_grammars.py
   ```

2. **Commit the grammar library** to your repository:
   ```bash
   git add grammars/my-languages.so
   git add grammars/my-languages.dylib  # if on macOS
   git commit -m "Add compiled grammar library"
   git push
   ```

   **Why commit the binary?** Building grammars on Streamlit Cloud can be slow and may fail. Pre-building and committing the `.so` file ensures reliable deployments.

### Step 2: Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Click "New app"
3. Connect your GitHub repository
4. Configure:
   - **Repository**: your-username/code-analyzer
   - **Branch**: main (or your default branch)
   - **Main file path**: app.py
   - **Python version**: 3.9 or higher

5. Click "Deploy"

### Step 3: Configure Secrets (Optional)

If you want to enable LLM analysis:

1. Go to your app's settings
2. Navigate to "Secrets"
3. Add your Gemini API key:
   ```toml
   GEMINI_API_KEY = "your-actual-api-key-here"
   ```
4. Click "Save"

### Step 4: Test Your Deployment

1. Wait for deployment to complete (2-5 minutes)
2. Visit your app URL (something like `https://username-code-analyzer.streamlit.app`)
3. Test with sample code:
   - Select Python
   - Paste example code
   - Click "Analyze Code"

## Alternative: Build on Cloud

If you prefer to build grammars on Streamlit Cloud (not recommended):

1. **Do NOT commit** the grammar binaries
2. Ensure these files are in your repo:
   - `packages.txt` (system dependencies)
   - `build_grammars.py` (build script)

3. Create a `startup.sh` script:
   ```bash
   #!/bin/bash
   python build_grammars.py
   ```

4. Update your Streamlit Cloud config to run this script first

**Note**: This approach is slower and may fail due to timeout issues.

## Troubleshooting Deployment Issues

### Issue: "Grammar library not found"

**Cause**: The `.so` file wasn't committed or wasn't built

**Solution**:
1. Build locally: `python build_grammars.py`
2. Commit: `git add grammars/*.so && git commit -m "Add grammars"`
3. Push: `git push`
4. Redeploy on Streamlit Cloud

### Issue: "Module not found" errors

**Cause**: Dependencies not installed

**Solution**:
1. Verify `requirements.txt` is in your repo
2. Check all dependencies are listed
3. Redeploy

### Issue: App is slow or times out

**Cause**: Building grammars on cloud or analyzing very large files

**Solution**:
1. Use pre-built grammars (commit `.so` file)
2. Limit file size for analysis
3. Reduce max visualization depth

### Issue: LLM features not working

**Cause**: API key not configured

**Solution**:
1. Add `GEMINI_API_KEY` to Streamlit secrets
2. Ensure the key is valid and has API access enabled
3. Check app logs for API errors

## Performance Optimization

### 1. Use Pre-built Grammars
Always commit compiled grammar libraries for faster deployments.

### 2. Optimize Visualization
Set reasonable defaults:
- Max depth: 8 levels
- Limit nodes for large files

### 3. Cache Heavy Operations
Add caching to parser initialization:
```python
@st.cache_resource
def initialize_parsers():
    # ... initialization code
```

### 4. Handle Timeouts
Add timeout handling for long-running operations:
```python
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Operation timed out")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(30)  # 30 second timeout
```

## Monitoring Your App

### Check App Health
- Monitor app logs in Streamlit Cloud dashboard
- Check resource usage (RAM, CPU)
- Review error reports

### User Analytics
- Track usage with Streamlit's built-in analytics
- Monitor API costs if using LLM features

### Update Strategy
1. Test changes locally first
2. Push to a dev branch
3. Deploy dev branch to test environment
4. Merge to main when stable

## Cost Considerations

### Streamlit Cloud
- **Free tier**: 1 private app + unlimited public apps
- **Team tier**: More resources and features

### Gemini API
- Gemini 2.0 Flash is free tier with generous limits
- 15 requests per minute (RPM) on free tier
- 1 million tokens per minute (TPM) on free tier
- Monitor usage at https://aistudio.google.com/
- Upgrade to paid tier for higher limits if needed

## Security Best Practices

1. **Never commit API keys** to your repository
2. **Use Streamlit secrets** for sensitive data
3. **Validate user input** to prevent injection attacks
4. **Rate limit** API calls to prevent abuse
5. **Monitor** for unusual usage patterns

## Scaling Considerations

If your app becomes popular:

1. **Upgrade Streamlit plan** for more resources
2. **Optimize parsing** for common use cases
3. **Add caching** aggressively
4. **Consider** splitting into microservices
5. **Implement** queue systems for heavy processing

## Support Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Community Forum](https://discuss.streamlit.io/)
- [Streamlit Cloud Status](https://status.streamlit.io/)
- [Tree-sitter Documentation](https://tree-sitter.github.io/)

## Backup and Recovery

### Backup Strategy
1. Keep grammar sources in git
2. Document build process
3. Version your dependencies
4. Export app settings

### Recovery Steps
1. Clone repository
2. Build grammars locally
3. Test locally before redeploying
4. Redeploy to Streamlit Cloud

---

## Quick Deployment Checklist

- [ ] Grammar library built and committed
- [ ] All dependencies in `requirements.txt`
- [ ] `packages.txt` includes system dependencies
- [ ] Repository pushed to GitHub
- [ ] App deployed on Streamlit Cloud
- [ ] Secrets configured (if using LLM)
- [ ] App tested with sample code
- [ ] Documentation updated
- [ ] Users notified of new version

Happy deploying! 🚀
// Load configuration from environment or config file
const path = require('path');

// Environment variable overrides
const config = {
  disableHotReload: process.env.DISABLE_HOT_RELOAD === 'true',
};

module.exports = {
  webpack: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
    configure: (webpackConfig) => {
      
      // Disable hot reload completely if environment variable is set
      if (config.disableHotReload) {
        // Remove hot reload related plugins
        webpackConfig.plugins = webpackConfig.plugins.filter(plugin => {
          return !(plugin.constructor.name === 'HotModuleReplacementPlugin');
        });
        
        // Disable watch mode
        webpackConfig.watch = false;
        webpackConfig.watchOptions = {
          ignored: /.*/, // Ignore all files
        };
      }
      
      return webpackConfig;
    },
  },
  devServer: {
    static: [
      {
        directory: path.join(__dirname, 'public'),
        publicPath: '/',
      },
    ],
    historyApiFallback: {
      disableDotRule: true,
      index: '/index.html',
    },
    setupMiddlewares: (middlewares, devServer) => {
      // Add middleware to serve manifest.json directly
      devServer.app.get('/manifest.json', (req, res) => {
        res.setHeader('Content-Type', 'application/json');
        res.sendFile(path.join(__dirname, 'public', 'manifest.json'));
      });
      
      devServer.app.get('/favicon.ico', (req, res) => {
        res.sendFile(path.join(__dirname, 'public', 'favicon.ico'));
      });
      
      devServer.app.get('/robots.txt', (req, res) => {
        res.sendFile(path.join(__dirname, 'public', 'robots.txt'));
      });
      
      return middlewares;
    },
  },
};
  

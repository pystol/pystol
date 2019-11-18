const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

// Mocking variables in webpack dev
const host = process.env.HOST || 'localhost';
const port = process.env.PORT || '8080';
const MockPod = require('./src/server/mocks/pod.json');
const MockService = require('./src/server/mocks/service.json');
const MockIngress = require('./src/server/mocks/ingress.json');

module.exports = {
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader"
                }
            },
            {
                test: /\.s?css$/,
                use: [
                    {
                        loader: "style-loader"
                    },
                    {
                        loader: "css-loader"
                    },
                    {
                        loader: "sass-loader"
                    },
                ]
            },
            // {
            //     test: /\.(png|jpg)$/,
            //     use: {
            //         loader: "url-loader?limit=8192"
            //     }
            // },
            {
                test: /\.(jpg|png|ttf|eot|svg)$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            name: './images/[path][name]-[hash:8].[ext]'
                        },
                    },
                ]
            },
        ]
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: "./src/index.html",
            filename: "./index.html"
        })
    ],
    devServer: {
        contentBase: path.join(__dirname, 'dist'),
        // 404 should break if true then all Api fallback will go to /
        historyApiFallback: false,
        // Enable hot reloading
        hot: true,
        host,
        port,
        proxy: {
          '/pod': {
            bypass: (request, response) => {
              if (request.url.substr(-4) === '/pod') {
                response.send(MockPod);
              }
            },
          },
          '/service': {
            bypass: (request, response) => {
              if (request.url.substr(-8) === '/service') {
                response.send(MockService);
              }
            },
          },
          '/ingress': {
            bypass: (request, response) => {
              if (request.url.substr(-8) === '/ingress') {
                response.send(MockIngress);
              }
            },
          },
          '/env-config.js': {
            bypass: (request, response) => {
              if (request.url.substr(-14) === '/env-config.js') {
                response.send("window._env_ = {PYSTOL_UI_API_HOST: '" + host + "',PYSTOL_UI_API_PORT: '" + port +"',}");
              }
            },
          },
        },
    }
}



const webpack = require('webpack');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const FileManagerPlugin = require('filemanager-webpack-plugin');

const config = {
    entry: {
        app : __dirname + '/js/index.jsx',
        //PorductList : __dirname + '/js/Product/product_list.jsx',
        //PorductPage : __dirname + '/js/Product/product_page.jsx',
    },
    output: {
        path: __dirname + '/dist',
        publicPath: '/dist/',
        filename: '[name].[contenthash].js',
    },
    resolve: {
        extensions: [".js", ".jsx", ".css", ".scss"]
    },
    plugins: [
        new CleanWebpackPlugin({
            cleanOnceBeforeBuildPatterns: ['*.js'],
        }),
        new webpack.DefinePlugin({ // <-- key to reducing React's size
            'process.env': {
                'NODE_ENV': JSON.stringify('production')
            }
        }),
        new webpack.HashedModuleIdsPlugin(),
        new HtmlWebpackPlugin({
            inject: 'body',
            template: './src/template/index.html',
            filename: '../index.html',
        }),
        new FileManagerPlugin({
            onEnd: {
                move:[
                    {source: 'index.html', destination: '../templates/index.html'},
                ]
            }
        }),
    ],
    module: {
        rules: [
            //sass, scss, css
            {
                test: /\.(s*)css$/,
                use: ['style-loader','css-loader','sass-loader']
            }
            ,
            //babel
            {
                test: [/\.jsx$/],
                exclude: /node_modules/,
                use: 'babel-loader',
            }
        ]
    },
    optimization: {
        runtimeChunk: 'single',
        splitChunks: {
            chunks: 'all',
            maxInitialRequests: Infinity,
            minSize: 0,
            cacheGroups: {
                vendor: {
                    test: /[\\/]node_modules[\\/]/,
                    name(module) {
                        // get the name. E.g. node_modules/packageName/not/this/part.js
                        // or node_modules/packageName
                        const packageName = module.context.match(/[\\/]node_modules[\\/](.*?)([\\/]|$)/)[1];
                        // npm package names are URL-safe, but some servers don't like @ symbols
                        return `npm.${packageName.replace('@', '')}`;
                    },
                },
            },
        },
    },
};

module.exports = config;


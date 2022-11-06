const path = require("path");
const webpack = require("webpack");
const common = require("./webpack.common");
const merge = require("webpack-merge");
const TerserJSPlugin = require('terser-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');

module.exports = merge(common ,{
    mode: "production",
    output: {
        filename: "[name].min.js",
        path: path.resolve(__dirname, './manager/static/dist/JS/')
    },
    optimization:{
        minimizer: [
            new TerserJSPlugin(),
            new OptimizeCSSAssetsPlugin()
        ],
    },
    plugins: [
        new MiniCssExtractPlugin({
          filename: '../CSS/[name].min.css',
        }),
        new webpack.ProvidePlugin({
          $: 'jquery',
          jQuery: 'jquery'
      })
    ],
    module: {
      rules: [
        {
          test: [/\.(scss)$/,/\.(css)$/],
          use: [            
            {
              // Adds CSS to the DOM by injecting a `<style>` tag
              loader: 'style-loader'
            },
            {              
              loader: MiniCssExtractPlugin.loader,
            },            
            {
              // Interprets `@import` and `url()` like `import/require()` and will resolve them
              loader: 'css-loader'
            },
            {
              // Loader for webpack to process CSS with PostCSS
              loader: 'postcss-loader',
              options: {
                plugins: function () {
                  return [
                    require('autoprefixer')
                  ];
                }
              }
            },
            {
              // Loads a SASS/SCSS file and compiles it to CSS
              loader: 'sass-loader'
            }
          ]
        }
      ]
    },
});
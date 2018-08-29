var path = require('path')
var webpack = require('webpack')

module.exports = {
  entry: './src/main.js',
  output: {
    path: path.resolve(__dirname, '../static/dist'),
    publicPath: '/dist/',
    filename: 'build.js'
  },
  module: {
    rules: [
      {test: /\.vue$/, loader: 'vue-loader', options: {loaders: {sass: 'vue-style-loader!css-loader!sass-loader?indentedSyntax'}}},
      {test: /\.js$/, loader: 'babel-loader', exclude: /node_modules/},
      {test: /(\.css$)/, loaders: ['style-loader', 'css-loader']},
      {test: /\.(png|woff|woff2|eot|ttf|svg)$/, loader: 'file-loader'},
      // {test: /\.js$/, loader: 'babel-loader', include: path.resolve(__dirname, 'node_modules', 'd3-downloadable')},
      // {test: /\.js$/, loader: 'babel-loader', include: path.resolve(__dirname, 'node_modules', 'svg-dataurl')}
    ]
  },
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js'
    },
    extensions: ['*', '.js', '.vue', '.json']
  },
  devServer: {
    historyApiFallback: true,
    noInfo: true,
    overlay: true,
    // port: 8000,
    host: '127.0.0.1'
  },
  performance: {
    hints: false
  },
  devtool: '#eval-source-map',
  node: {
    fs: 'empty',
    net: 'empty',
    tls: 'empty',
    dns: 'empty'
  }
}

if (process.env.NODE_ENV === 'production') {
  module.exports.devtool = '#source-map'
  // http://vue-loader.vuejs.org/en/workflow/production.html
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"production"'
      }
    }),
    new webpack.optimize.UglifyJsPlugin({
      sourceMap: true,
      compress: {
        warnings: false
      }
    }),
    new webpack.LoaderOptionsPlugin({
      minimize: true
    })
  ])
}

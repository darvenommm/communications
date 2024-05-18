import path from 'path';
import type { Configuration } from 'webpack';

// environment variables
const IS_DEVELOPMENT = (process.env.MODE ?? 'development') === 'development';

// call app paths
const callAppDirectoryPath = path.join(__dirname, '..', 'apps', 'calls');
const callAppStaticDirectoryPath = path.join(callAppDirectoryPath, 'static', 'calls', 'js');
const createCallAppTsPath = (...paths: string[]): string => {
  const fileName = paths.at(-1);
  paths = paths.slice(0, -1);

  return path.join(callAppDirectoryPath, 'ts', 'scripts', ...paths, `${fileName}.ts`);
};

const config: Configuration = {
  mode: IS_DEVELOPMENT ? 'development' : 'production',
  entry: {
    online_subscribers: createCallAppTsPath('subscribers', 'main'),
    call_offers: createCallAppTsPath('call_offers', 'main'),
    call_rooms: createCallAppTsPath('call_rooms', 'main'),
  },
  devtool: IS_DEVELOPMENT ? 'source-map' : false,
  output: {
    path: callAppStaticDirectoryPath,
    filename: '[name].js',
  },
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    extensions: ['.ts', '.js'],
  },
};

export default config;

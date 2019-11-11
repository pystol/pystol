module.exports = {
  root: true,
  plugins: [
    "eslint-plugin-jest",
      "react",
      "react-native",
//    "eslint-plugin-react",
  ],
  env: {
    // this section will be used to determine which APIs are available to us
    // (i.e are we running in a browser environment or a node.js env)
    node: true,
    browser: true
  },
  parserOptions: {
    parser: "babel-eslint",
    // specifying a module sourcetype prevent eslint from marking import statements as errors
    sourceType: "module",
    ecmaVersion: 6,
  },
  extends: [
    // use the recommended rule set for both plain javascript
    "eslint:recommended",
    "plugin:jest/recommended",
    "plugin:react/recommended"
  ],
  rules: {
    // we should always disable console logs and debugging in production
    "no-console": process.env.NODE_ENV === "production" ? "error" : "off",
    "no-debugger": process.env.NODE_ENV === "production" ? "error" : "off",
    "jest/no-disabled-tests": "warn",
    "jest/no-focused-tests": "error",
    "jest/no-identical-title": "error",
    "jest/prefer-to-have-length": "warn",
    "jest/valid-expect": "error"
  }
};

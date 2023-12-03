/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    'client/templates/client/*.html',
    'core/templates/core/*.html',
    'core/templates/core/partials/*.html',
    'dashboard/templates/dashboard/*.html',
    'lead/templates/lead/*.html',
    'teams/templates/teams/*.html',
    'userprofile/templates/userprofile/*.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}


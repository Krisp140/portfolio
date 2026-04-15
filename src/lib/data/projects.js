export const projects = [
  {
    title: 'BikeWatch: BlueBike Demand Map',
    description:
      'Interactive Mapbox visualization of BlueBike station demand with time filtering and isochrone overlays.',
    image: '/images/bike.avif',
    tags: ['Mapbox', 'D3', 'Data Visualization'],
    link: 'https://krisp140.github.io/bikewatch/',
    featured: true,
    year: 2026,
    story:
      'I mapped every BlueBike station in Boston and Cambridge, coloring them by net demand (arrivals vs departures) and sizing by total ridership. A time slider lets you scrub through hours of the day, and clicking a station reveals a cycling isochrone showing how far you can ride in 5, 10, or 15 minutes.'
  },
  {
    title: 'COVID-19 Visualization Redesign',
    description:
      'A critique and redesign of the NYT spiral COVID-19 chart. Features an interactive 3D terrain visualization built with Three.js mapping case volume and fatality rate.',
    image: '/A3/nyt.png',
    tags: ['Data Visualization', 'Three.js', 'D3', '3D'],
    link: '/A3/',
    featured: true,
    year: 2026,
    story:
      'The New York Times published a spiral chart to show COVID-19 trends, but its novelty made it hard to read. I redesigned it as a 3D terrain map where elevation encodes case volume and color encodes fatality rate, making spatial patterns immediately visible.'
  },
  {
    title: 'Boston Housing EDA',
    description:
      'An exploratory data analysis of the Boston Housing dataset. Interactive Plotly charts examine correlations between socioeconomic factors and median home values.',
    image: '/images/housing.jpg',
    tags: ['Data Visualization', 'Plotly', 'Python', 'EDA'],
    link: '/A2/',
    featured: true,
    year: 2026,
    story:
      'I explored the classic Boston Housing dataset to understand how factors like crime rate, distance to employment centers, and pupil-teacher ratio affect home values. Interactive scatter plots and heatmaps revealed surprising non-linear relationships.'
  },
  {
    title: 'Abortion Access & Displacement',
    description:
      'A persuasive visualization exploring how state-level abortion restrictions force patients to travel across borders, using dumbbell charts and scatter plots built with D3.',
    image: '/images/abortion.png',
    tags: ['D3', 'Data Visualization', 'Persuasion'],
    link: '/A4/',
    featured: true,
    year: 2026,
    story:
      'I examined CDC data on abortion rates by state of residence versus state of occurrence to reveal how restrictive laws displace patients rather than reduce abortions. Dumbbell charts highlight the gap, while a scatter plot connects policy strictness to cross-border travel.'
  },
  {
    title: 'Portfolio Website',
    description:
      'A personal portfolio site built with SvelteKit featuring an editorial brutalist design, dark/light themes, and scroll-driven animations.',
    image: 'https://placehold.co/600x340/0a0a0a/f5f2ed?text=Portfolio',
    tags: ['SvelteKit', 'CSS', 'Design'],
    link: null,
    featured: false,
    year: 2025,
    story:
      'I wanted a portfolio that felt like a printed magazine — bold typography, wire-grid backgrounds, and grayscale images that reveal color on hover. Built with SvelteKit and deployed to GitHub Pages.'
  },
  {
    title: 'Task Tracker',
    description:
      'A task management app for organizing daily work. Features include creating, completing, filtering, and archiving tasks with local storage persistence.',
    image: 'https://placehold.co/600x340/0a0a0a/f5f2ed?text=Task+Tracker',
    tags: ['JavaScript', 'HTML', 'CSS'],
    link: null,
    featured: false,
    year: 2024,
    story:
      'Built as my first serious JavaScript project, this tracker taught me about DOM manipulation, event delegation, and persisting state with localStorage. Simple but functional.'
  },
  {
    title: 'Weather Dashboard',
    description:
      'A weather application that fetches real-time data from a public API and displays forecasts with a clean interface.',
    image: 'https://placehold.co/600x340/0a0a0a/f5f2ed?text=Weather+App',
    tags: ['JavaScript', 'REST API', 'CSS'],
    link: null,
    featured: false,
    year: 2024,
    story:
      'My introduction to working with REST APIs. Fetching weather data, handling loading states, and displaying forecasts taught me the async patterns I still use today.'
  },
  {
    title: 'Transit Accessibility Map',
    description:
      'An interactive map visualizing public transit accessibility across Boston neighborhoods, highlighting gaps in service for mobility-impaired residents.',
    image: 'https://placehold.co/600x340/0a0a0a/f5f2ed?text=Transit+Map',
    tags: ['D3', 'GeoJSON', 'Accessibility'],
    link: null,
    featured: false,
    year: 2025,
    story:
      'After reading about wheelchair users stranded by broken elevators at MBTA stations, I mapped every station\'s accessibility status against neighborhood demographics. The result revealed that the least accessible stations serve the communities that depend on transit the most.'
  },
  {
    title: 'Rent vs. Income Visualization',
    description:
      'A scrollytelling piece examining how rent burden has shifted across U.S. metro areas over the past decade using Census ACS data.',
    image: 'https://placehold.co/600x340/0a0a0a/f5f2ed?text=Rent+vs+Income',
    tags: ['D3', 'Scrollytelling', 'Census Data'],
    link: null,
    featured: false,
    year: 2026,
    story:
      'Census data shows that median rent has outpaced median income in nearly every major metro since 2015. I built a scrolling narrative that walks readers through the divergence, city by city, using animated area charts.'
  },
  {
    title: 'Election Results Dashboard',
    description:
      'A real-time dashboard for tracking election night results with county-level choropleth maps and vote margin indicators.',
    image: 'https://placehold.co/600x340/0a0a0a/f5f2ed?text=Election+Dashboard',
    tags: ['D3', 'TopoJSON', 'Real-time'],
    link: null,
    featured: false,
    year: 2024,
    story:
      'Election night maps often obscure how close races really are. I designed a dashboard that uses graduated color scales and margin bars so viewers can immediately see which counties are competitive and which are decided.'
  },
  {
    title: 'Climate Change Data Story',
    description:
      'An interactive data story exploring 150 years of global temperature anomalies, sea level rise, and CO2 concentration trends.',
    image: 'https://placehold.co/600x340/0a0a0a/f5f2ed?text=Climate+Story',
    tags: ['D3', 'SVG Animation', 'Data Journalism'],
    link: null,
    featured: false,
    year: 2025,
    story:
      'I combined NASA GISS temperature data with NOAA CO2 records to build an animated timeline showing how temperature anomalies track carbon concentration. The hockey-stick curve is even more striking when you watch it draw itself.'
  }
];

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
    title: 'Boston Evictors',
    description:
      'Interactive data visualization exploring eviction activity in Boston through neighborhood patterns, landlord behavior, and housing instability signals.',
    image: '/images/boston-evictors.png',
    tags: ['D3', 'Data Visualization', 'Housing'],
    link: 'https://carol1120chen.github.io/boston_evictors_vis_data_fp/#overview',
    featured: true,
    year: 2026,
    story:
      'This project examines eviction activity across Boston, using interactive views to connect landlord filings, neighborhood concentration, and broader housing vulnerability. The visualization helps make spatial and ownership patterns easier to compare at a glance.'
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
  }
];

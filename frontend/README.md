# AI on FHIR Query Interface - Frontend

A React-based user interface for querying FHIR-compliant patient data using natural language queries.

## Overview

This application provides an intuitive interface for healthcare professionals to search patient records using natural language. It converts queries like "Show me all diabetic patients over 50" into structured FHIR API requests and displays results in user-friendly formats.

## Features

### Core Functionality

- **Natural Language Query Input**: Type queries in plain English with auto-complete suggestions
- **Real-time Suggestions**: Get query suggestions as you type (debounced for performance)
- **Advanced Filters**: Refine searches using:
  - Age range filters (0-18, 19-35, 36-60, 60+) (Needs Improvements)
  - Gender filters (Male, Female, Other)
  - Diagnosis code filters
- **Data Visualization**:
  - Interactive charts showing patient demographics and distributions
  - Sortable, paginated data tables displaying patient records
- **Query Results Summary**: View total patients found and confidence scores
- **Filter Display**: See both parsed and applied filters for transparency

### Technical Features

- Built with **Next.js 14** and **React 18**
- **TypeScript** for type safety
- **TanStack Query (React Query)** for efficient data fetching and caching
- **Tailwind CSS** for responsive, modern UI
- **shadcn/ui** components for accessible, customizable UI elements
- **Recharts** for data visualization
- **Lucide React** for icons

## Prerequisites

- Node.js 18+ and npm/yarn/pnpm
- Backend API server running (see backend README)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd frontend
```

2. Install dependencies:

```bash
pnpm install
```

3. Configure environment variables:
   Create a `.env.local` file in the root directory:

```env

```

4. Start the development server:

```bash
pnpm dev
```

## Usage Examples

### Basic Query

1. Type a natural language query in the search box:
   - "Show me all female patients over 50"
   - "Find diabetic patients under 30"
   - "List patients with hypertension"

2. Click "Search" or press Enter to submit

3. Results display with:
   - Summary statistics
   - Visual charts
   - Detailed patient table

## Key Components

### FilterControls

- Dynamic filter dropdowns for age, gender, and diagnosis
- Syncs with backend-provided filter options

### PatientsTable

- Sortable columns
- Pagination support
- Displays patient demographics and conditions

### AnalyticsCharts

- Visual representation of patient data
- Age distribution, gender breakdown, etc.
- Built with Recharts

### FiltersDisplay

- Shows parsed filters from NLP processing
- Displays applied filters for transparency

## Development Notes

### State Management

- Uses React Query for server state management
- Local state with React hooks for UI state
- Filters sync between local state and backend responses

### Performance Optimizations

- Query debouncing (300ms) for auto-complete
- React Query caching with stale-time configurations
- Lazy loading of chart data

### Type Safety

- Full TypeScript coverage
- API types generated from OpenAPI schema
- Strict type checking enabled

## What I Focused On

1. **User Experience**: Intuitive interface with real-time feedback and clear data presentation
2. **Performance**: Efficient data fetching with caching and debouncing
3. **Type Safety**: Comprehensive TypeScript implementation
4. **Accessibility**: Using shadcn/ui components built on Radix UI primitives
5. **Code Organization**: Clean separation of concerns with reusable components

## Areas for Improvement (Given More Time)

1. **Enhanced Error Handling**: More granular error messages and retry logic
2. **Testing**: Add unit tests (Jest) and E2E tests (Playwright/Cypress)
3. **Fix Autocomplete**: Improve suggestion dropdown UX with proper keyboard navigation and selection handling
4. **Fix Filter Selection**: Resolve Select component state management issues to ensure filter preferences update correctly
5. **Advanced Filtering**: Support for date ranges, complex conditions, and filter combinations
6. **Export Functionality**: Allow users to export results to CSV/PDF
7. **Query History**: Save and retrieve previous queries
8. **Internationalization**: Multi-language support (i18n)
9. **Offline Support**: PWA capabilities with service workers
10. **Advanced Analytics**: More chart types and drill-down capabilities
11. **Real-time Updates**: WebSocket integration for live data updates
12. **Accessibility Audit**: WCAG 2.1 AA compliance verification

## Building for Production

```bash
pnpm run build
pnpm run start
```

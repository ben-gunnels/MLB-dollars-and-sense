### General Overview

The application is comprised of two basic parts: 1. Data Collection and Analysis 2. .NET Application Interface.

The first part, the data collection, can be found in the scrapers directory and is composed of methods for scraping data from Baseball Reference and data from the Cot's salary data sheet. 

The second part is the main application in the ASP.NET framework. The layout uses Razor pages to manage the frontend and backend of the application. 

### Startup
The user should ensure that they have .NET capability installed, preferably with Visual Studio Code. See https://dotnet.microsoft.com/en-us/download for .NET. The application uses SQLite to manage the database, ensure that it is installed on the project via:

```dotnet add package Microsoft.EntityFrameworkCore.Sqlite```

To start the application navigate to the root of the application BaseballApp and run:

```dotnet run```

### Application Overview
When a user starts the application they are greeted by the home page which contains top performing baseball players by value for the year 2024.



### Data Methodology

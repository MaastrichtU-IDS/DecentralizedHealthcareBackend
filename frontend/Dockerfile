# Use an official nginx image as a parent image
FROM node:20 as build

WORKDIR /app

RUN npm install --global expo-cli

ADD . .

RUN npm install && \
    expo build:web


FROM nginx:alpine

# Copy the build output from your Expo web app to the nginx html directory
COPY --from=build /app/web-build/ /usr/share/nginx/html

# Expose port 80 to the outside world
EXPOSE 80

# Start nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]

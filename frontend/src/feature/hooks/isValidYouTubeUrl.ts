export const isValidYouTubeUrl = (url: string): boolean => {
  const youTubeUrlRegex =
    /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+$/;
  return youTubeUrlRegex.test(url);
};

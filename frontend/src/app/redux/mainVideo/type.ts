interface UserState {
  img_url: string;
  position: number;
  description: string;
  desableButton: boolean;
  panelType: "none" | "loading" | "img" | "video";
}

export default UserState;

interface UserState {
  img_url: string;
  position: number;
  description: string;
  desableButton: boolean;
  panelType: "none" | "img" | "video";
}

export default UserState;

<template>
  <div>
    <el-container>
      <el-header>Spare Chats</el-header>
      <el-main>
        <el-row :gutter="20" justify="center">
          <el-col
            :span="20"
            :lg="20"
            style="margin-left: auto; margin-right: auto"
          >
            <el-card
              shadow="hover"
              style="height: 70vh; background-color: blue"
            >
              <el-row :gutter="20">
                <el-col :span="20" :md="10" :offset="2" style="">
                  <div class="grid-content bg-purple">
                    <h3 style="color: white">Create Room</h3>
                    <el-card
                      shadow="hover"
                      style="height: 45vh; margin-top: 5vh"
                    >
                      <room-form></room-form>
                    </el-card>
                  </div>
                </el-col>

                <el-col :span="24" :md="10" class="hidden-sm-and-down" style="">
                  <div class="grid-content bg-purple">
                    <h3 style="color: white">Join Room</h3>
                    <el-card
                      shadow="hover"
                      style="height: 45vh; margin-top: 5vh"
                    >
                      <join-room-form></join-room-form>
                    </el-card>
                  </div>
                </el-col>
              </el-row>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import RoomForm from "@/components/LandingPageComponent/CreateRoomForm";
import JoinRoomForm from "@/components/LandingPageComponent/JoinRoomForm";

export default {
  components: { RoomForm, JoinRoomForm },
};
</script>
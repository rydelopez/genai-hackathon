import { Divider } from "@nextui-org/react";
import ConversationTable from "./components/Table";

export default async function Home() {
  const conversation_id = "123";

  const { avg_response_length, unique_words, response_time, q_and_a } = await fetch(
    `http://localhost:3500/stats/conversation/${conversation_id}`
  ).then((res) => res.json());

  return (
    <div className="p-4 md:p-10 mx-auto max-w-7xl flex flex-col">
      <div className="flex h-5 items-center space-x-4 text-small justify-center">
        <div>Average response length: {avg_response_length} characters</div>
        <Divider orientation="vertical" />
        <div>Unique response length: {unique_words} characters</div>
        <Divider orientation="vertical" />
        <div>Response time: {response_time} seconds</div>
      </div>
      <div className="flex justify-center items-center py-8">
        <ConversationTable data={q_and_a} />
      </div>
    </div>
  );
}

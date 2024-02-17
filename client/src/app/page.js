export default async function Home() {
  const conversation_id = "123";

  const { avg_response_length, unique_length, response_time } = await fetch(
    `http://localhost:3500/stats/conversation/${conversation_id}`
  ).then((res) => res.json());

  return (
    <div className="p-4 md:p-10 mx-auto max-w-7xl">
      <h1>Hello</h1>
      <p>
        Average response length: {avg_response_length} characters
      </p>
      <p>
        Unique response length: {unique_length} characters
      </p>
      <p>
        Response time: {response_time} seconds
      </p>
    </div>
  );
}
